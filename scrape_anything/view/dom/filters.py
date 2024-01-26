import pandas as pd
import re
import base64
import io
from PIL import Image
import imagehash
from scrape_anything.util.io import stringable_dataframe_to_csv, dataframe_to_stringable


def is_css_code(text):
    pattern = r"\{.*?\}"

    # Find all matches of CSS rules in the text
    matches = re.findall(pattern, text)

    # Print the matched CSS rules
    for match in matches:
        return True
    return False


def get_all_clickable(df):
    df["clickable"] = (
        (df["cursor"] == "pointer")
        | (df.onclick_no_null == True)
        | (df.ElementType == "BUTTON")
        | (df.ElementType == "A")
    )

    _df = df[df["clickable"]].copy()
    return _df


def drop_with_exists_finer_element(df):
    df.parent_xpath = df.parent_xpath.fillna("")
    indexs_to_drop = list()
    for index, row in df.iterrows():
        sub_elements = df[df.parent_xpath.str.startswith(f"{row['parent_xpath']}/")]
        drop_row = any(sub_elements.textContent.apply(lambda x: x in row.textContent))
        if drop_row:
            indexs_to_drop.append(index)
    return df.drop(index=indexs_to_drop)


def remove_elements_without_size(df):
    _df = df[(~df.width.isna()) & (~df.height.isna())]
    _df.loc[:, "width"] = (
        pd.to_numeric(_df.loc[:, "width"], errors="coerce").fillna(0.0).astype(float)
    )
    _df.loc[:, "height"] = (
        pd.to_numeric(_df.loc[:, "height"], errors="coerce").fillna(0.0).astype(float)
    )
    return _df[(_df.width > 0) & (_df.height > 0)]


def remove_out_of_window(df, viewpointscroll, viewportHeight):
    # height,width,top,bottom
    df.bottom = pd.to_numeric(df.bottom, errors="coerce").fillna(0.0).astype(float)
    df.top = pd.to_numeric(df.top, errors="coerce").fillna(0.0).astype(float)
    return df[
        (df.top >= viewpointscroll) & (df.bottom < (viewpointscroll + viewportHeight))
    ]


def remove_without_textual_infomration(df):
    # remove if all is null
    _df = df[
        ~df[
            [
                "data-initial-value",
                "TooltipValue",
                "innerText",
                "textContent",
                "AriaLabel",
            ]
        ]
        .isna()
        .all(axis=1)
    ]
    # keep if any contains a value
    return _df[
        (_df.innerText != "")
        | (_df["data-initial-value"] != "")
        | (_df.TooltipValue != "")
        | (_df.textContent != "")
        | (_df.AriaLabel != "")
    ]


def minimize_page_data(df, viewpointscroll, viewportHeight, using_vision=False):
    _df = df.copy()
    _df = remove_elements_without_size(_df)
    _df = remove_out_of_window(_df, viewpointscroll, viewportHeight)
    _df = remove_without_textual_infomration(_df)

    # if all the information is the same, take the deeper element (which is the last becuase of our listing method)
    _df.drop_duplicates(
        subset=["textContent", "TooltipValue", "AriaLabel", "data-initial-value"],
        keep="last",
        inplace=True,
    )

    # remove JS comments
    _df.textContent = _df.textContent.apply(lambda x: str(x).split("//#")[0])
    # remove elements contains css code
    _df = _df.loc[
        (_df["textContent"].apply(is_css_code) == False) | _df.textContent.isna()
    ]
    clickable_df = get_all_clickable(_df)
    _df = drop_with_exists_finer_element(_df)
    _df = pd.concat([_df, clickable_df])
    if not using_vision:
        _df.drop(
            columns=[
                "parent_xpath",
                "height",
                "width",
                "top",
                "bottom",
                "left",
                "right",
            ],
            inplace=True,
        )
    _df.drop(columns=["cursor", "onclick_no_null"], inplace=True)
    #
    return _df


def dataframe_diff(df_before, df_current):
    """
    Calculates the difference between two DataFrames.
    Returns two DataFrames: one for removed rows and one for added rows.
    """
    if df_before is None:
        return None, None
    df1_list = (
        stringable_dataframe_to_csv(df_before).to_csv(index=False).split("\n")[1:]
    )
    df2_list = (
        stringable_dataframe_to_csv(df_current).to_csv(index=False).split("\n")[1:]
    )

    added_to_changed = dataframe_to_stringable(
        pd.DataFrame(
            [row.split(",") for row in df2_list if row not in df1_list],
            columns=list(df_before.columns),
        )
    )
    removed = dataframe_to_stringable(
        pd.DataFrame(
            [row.split(",") for row in df1_list if row not in df2_list],
            columns=list(df_before.columns),
        )
    )

    return added_to_changed, removed


def is_screenshot_changed(screen_strem_before, screen_strem_current):
    if screen_strem_before is None:
        return None
    img1 = Image.open(io.BytesIO(base64.b64decode(screen_strem_before)))
    img2 = Image.open(io.BytesIO(base64.b64decode(screen_strem_current)))

    # Compute hashes
    hash1 = imagehash.dhash_vertical(img1)
    hash2 = imagehash.dhash_vertical(img2)

    # Compare hashes
    return hash1 - hash2 != 0
