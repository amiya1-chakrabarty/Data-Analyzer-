# Core Pkgs
import streamlit as st 

# EDA Pkgs
import pandas as pd 
import numpy as np 


# Data Viz Pkg
import matplotlib.pyplot as plt 
import matplotlib
matplotlib.use("Agg")
import seaborn as sns 



def main():
    """Semi Automated ML App with Streamlit """
    st.title("Data Analysis App")
    activities = ["Data Exploration","Data Quality Validation","Data Visualization"]
    choice = st.sidebar.selectbox("Select Activities",activities)

    if choice == 'Data Exploration':
        st.subheader("Data Exploration")

        data = st.file_uploader("Upload a Dataset", type=["csv", "txt"])
        if data is not None:
            df = pd.read_csv(data)
            st.dataframe(df)
            
            if st.checkbox("Top 5 and last 5 records"):
                st.write(df.head())
                st.write(df.tail())
            
            if st.checkbox("Data Dimensions"):
                st.write("Number of Rows: "+str(df.shape[0]))
                st.write("Number of Columns: "+str(df.shape[1]))


            if st.checkbox("Column names"):
                all_columns = df.columns.to_list()
                st.write(all_columns)

            if st.checkbox("Statistical summary"):
                st.write(df.describe())

            if st.checkbox("Show Selected Columns"):
                all_columns = df.columns.to_list()
                selected_columns = st.multiselect("Select Columns",all_columns)
                new_df = df[selected_columns]
                st.dataframe(new_df)
                
            if st.checkbox("Numeric columns"):
                st.write(df.select_dtypes(include=['int16', 'int32', 'int64', 'float16', 'float32', 'float64']).columns.tolist())

            if st.checkbox("Categorical columns"):
                st.write(df.select_dtypes(exclude=['int', 'float']).columns)
                
            if st.checkbox("Categories in categorical columns"):
                df1 = df.select_dtypes(exclude=['int', 'float'])
                for col in df1.columns:
                    st.write(df1[col].value_counts())
                

                             
    elif choice == 'Data Quality Validation':
        st.subheader("Data quality validation")
        data = st.file_uploader("Upload a Dataset", type=["csv", "txt", "xlsx"])
        if data is not None:
            df = pd.read_csv(data)
            st.dataframe(df.head())
            
            if st.checkbox("Missing Value Counts"):
                st.write(df.isnull().sum())
                
            if st.checkbox("Outliers count in each column"):
                Q1 = df.quantile(0.25)
                Q3 = df.quantile(0.75)
                IQR = Q3 - Q1
                st.write(((df < (Q1 - 1.5 * IQR)) | (df > (Q3 + 1.5 * IQR))).sum()) 
                
            if st.checkbox("Distribution details"):
                df1 = df.select_dtypes(include=['int', 'float'])
                all_columns = df1.columns.to_list()
                column_to_plot = st.selectbox("Select 1 Column",all_columns)
                st.write("Skewness: %f" % df[column_to_plot].skew())
                st.write("Kurtosis: %f" % df[column_to_plot].kurt())
                st.write('***If skewness is less than -1 or greater than 1, the distribution is highly skewed.If skewness is between -1 and -0.5 or between 0.5 and 1, the distribution is moderately skewed.If skewness is between -0.5 and 0.5, the distribution is approximately symmetric.A standard normal distribution has kurtosis of 3 ***')   
                

    elif choice == 'Data Visualization':
        st.subheader("Data Visualization")
        data = st.file_uploader("Upload a Dataset", type=["csv", "txt", "xlsx"])
        if data is not None:
            df = pd.read_csv(data)
            st.dataframe(df.head())
            
            if st.checkbox("Correlation Plot(Seaborn)"):
                st.write(sns.heatmap(df.corr(),annot=True))
                st.pyplot()


        # Customizable Plot

            all_columns_names = df.columns.tolist()
            type_of_plot = st.selectbox("Select Type of Plot",["area","bar","line","hist","box"])
            selected_columns_names = st.multiselect("Select Columns To Plot",all_columns_names)

            if st.button("Generate Plot"):
                st.success("Generating Customizable Plot of {} for {}".format(type_of_plot,selected_columns_names))

                # Plot By Streamlit
                if type_of_plot == 'area':
                    cust_data = df[selected_columns_names]
                    st.area_chart(cust_data)

                elif type_of_plot == 'bar':
                    cust_data = df[selected_columns_names]
                    st.bar_chart(cust_data)

                elif type_of_plot == 'line':
                    cust_data = df[selected_columns_names]
                    st.line_chart(cust_data)

                # Custom Plot 
                elif type_of_plot:
                    cust_plot= df[selected_columns_names].plot(kind=type_of_plot)
                    st.write(cust_plot)
                    st.pyplot()
                    
if __name__ == '__main__':
    main() 
