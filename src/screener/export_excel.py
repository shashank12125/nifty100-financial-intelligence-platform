import pandas as pd

def export_screeners(results):

    output_file = "output/screener_output.xlsx"

    with pd.ExcelWriter(output_file) as writer:

        for preset, df in results.items():

            df.to_excel(
                writer,
                sheet_name=preset[:31],
                index=False
            )

    print(f"\nExcel Generated : {output_file}")