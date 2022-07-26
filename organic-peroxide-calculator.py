import csv
import os
import pandas as pd

sub_info_df = pd.read_csv("Substance_Information.csv")                                # creating a pandas df for the json data
org_perx_df = pd.read_csv("Product_List.csv")                                # creating a pandas df for the json data
new_df = org_perx_df.merge(sub_info_df, on="CAS", how="right", indicator=True).drop("_merge", axis="columns")


class OrgPeroxideCalculator:
    def __init__(self):
        o_o_grps_num = self.o_o_grps_num
        hydrogen_conc = self.hydrogen_conc
        mol_mass = self.mol_mass
        oxygen_conc = self.oxygen_conc

    @staticmethod
    def intm_calculator(self, x, y, z):

        return x * (y/100) / z


    @staticmethod
    def intm_oa_calculator(self, df):

        org = OrgPeroxideCalculator
        oa_list = []
        for index, row in df.iterrows():
            oo_grps = row["Number of O-O groups"]
            mol_mass = row["Molecular Mass"]
            max_conc = row["max (%)"]
            intm_oa = org.intm_calculator(self, oo_grps, max_conc, mol_mass)
            oa_list.append(intm_oa)

        return oa_list

    @staticmethod
    def df_maker(self, df):

        org = OrgPeroxideCalculator
        df["Calculated Oxygen Concentration"] = org.intm_oa_calculator(self, df)
        with pd.option_context('display.max_rows', None, 'display.max_columns',
                               None):  # more options can be specified also

            return df

    @staticmethod
    def id_retriever(self, df):
        org = OrgPeroxideCalculator
        id_list = []
        for index, row in df.iterrows():
            prod_id = row["Product ID"]
            id = prod_id[-1]
            id_list.append(id)

        return id_list

    def id_maker(self, df):

        org = OrgPeroxideCalculator
        df = df.drop("Product ID_y", axis=1)
        df["Product ID"] = df["Product ID_x"]
        df = df.drop("Product ID_x", axis=1)
        df.sort_values(by=["Product ID"], inplace=True)
        id_df = df
        id_list = org.id_retriever(self, id_df)
        id_df["ID"] = id_list

        return id_df

    @staticmethod
    def h2o2_conc_calculator(self, series):

        df = series.to_frame()
        o2_conc_list = []
        for index, row in df.iterrows():
            a = row["Calculated Oxygen Concentration"]
            if a < (0.5 / 100.0):
                b = "Yes"
            else:
                b = "No"
            o2_conc_list.append(b)

        df["Organic Peroxide (Yes / No)"] = o2_conc_list

        return df


org = OrgPeroxideCalculator
intm_df = org.df_maker(1, new_df)
intm_df = org.id_maker(1, intm_df)

oa_sum_series = intm_df.groupby(["Product ID"])["Calculated Oxygen Concentration"].sum()
oa_sum_series = oa_sum_series.apply(lambda row: row * 16.0)
oa_df = org.h2o2_conc_calculator(1, oa_sum_series)

print(oa_sum_series)
print(oa_df)

