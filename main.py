import os
import pandas as pd
import streamlit as st


def main():

    path = "data"
    files = os.listdir(path)
    strategies = [f for f in files if os.path.isdir(os.path.join(path, f))]

    df_concat = pd.DataFrame()
    for strategy in strategies:
        # df = pd.read_csv(f"data/{strategy}/9432/performance_summary.csv", names=["項目","すべて ¥","すべて %","ロング ¥","ロング %","ショート ¥","ショート %"], encoding="UTF-8")
        df = pd.read_csv(f"data/{strategy}/9432/performance_summary.csv", index_col=0, encoding="UTF-8")
        # df = df.set_index("Unnamed: 0")
        df = df.T
        df = df.reset_index()
        df = df.rename(columns={"index":"項目"})
        df.insert(0, "ストラテジー", strategy) 
        df = df.set_index(["ストラテジー", "項目"])
        df_concat = pd.concat([df_concat, df])
    df_concat = df_concat[df_concat.index.get_level_values("項目").isin(["すべて ¥"])]
    df_concat = df_concat.sort_values("純利益", ascending=False)
    df_concat = df_concat[["純利益", "総利益", "総損失", "最大ドローダウン", "プロフィットファクター", "終了したトレードの合計", "勝率"]]
    df_concat = df_concat.astype({"純利益" : int, "総利益" : int, "総損失" : int, "最大ドローダウン" : int, "終了したトレードの合計" : int})
    df_concat = df_concat.round({"プロフィットファクター" : 2, "勝率" : 2})
    df_concat = df_concat.reset_index()
    df_concat = df_concat.set_index("ストラテジー")
    df_concat = df_concat.drop("項目", axis=1)
    df_concat = df_concat.rename(columns={"終了したトレードの合計": "トレード数"})

    # st.set_page_config(layout="wide")
    st.header("TradingView レポート")
    st.subheader("ストラテジー比較")
    st.dataframe(df_concat.style.format({"プロフィットファクター" : "{:.2f}", "勝率" : "{:.2f}"}), 2000, 1500)
    # st.dataframe(df_concat)
    # st.table(df_concat)


if __name__ == '__main__':
    main()
