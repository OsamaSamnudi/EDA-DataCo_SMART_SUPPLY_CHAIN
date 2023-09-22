import streamlit as st

st.set_page_config(
    layout = 'wide' ,
    page_title = 'Data CO SMART SUPPLY CHAIN',
    page_icon ='📊')
# ______________________________________________________________________________________________________________________________________________________________________________________________________
# Import Libraries
import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from datasist.structdata import detect_outliers
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# Read Data
path = 'DataCoSupplyChainDataset.csv'
Old_df = pd.read_csv(path ,encoding="ISO-8859-1", low_memory=False)
df = pd.read_csv('New DataCoSupplyChain.csv',index_col=0)
pd.options.display.float_format ='{:,.2f}'.format

for i in df.columns:
    if df[i].dtype == 'int64':
        df[i] = df[i].astype('int32')
    elif df[i].dtype == 'float64':
        df[i] = df[i].astype('float32')
    else:
        df[i] = df[i]

# Outliers Detection :
from datasist.structdata import detect_outliers
outliers_dict = {}
for i in df.select_dtypes(include='number').columns:
    outliers_indices = detect_outliers(df, 0, [i])
    outliers_dict[i] = len(outliers_indices)
df_outliers = pd.DataFrame.from_dict(outliers_dict, orient='index', columns=['Outliers']).sort_values('Outliers',ascending=False).reset_index()
Outlier_lst = df_outliers[df_outliers['Outliers'] != 0]

# Sidebar
brief = st.sidebar.checkbox(":red[Brief about Supply Chain]")
Planning = st.sidebar.checkbox(":orange[About Project]")
About_me = st.sidebar.checkbox(":green[About me]")

if brief:
    st.sidebar.header(":red[Brief about Supply Chain]")
    st.sidebar.write("""
    # What is supply chain management?
    * Supply chain management refers to the coordination and oversight of various activities involved in the production, distribution, and delivery of goods or services from their source to the end consumer.
      This entails everything from sourcing the raw components for a product to delivering the final result directly to the consumer.
      Part of working in supply chain management is figuring out how your company can maximize productivity, sustain production, grow within the market, and provide the most convenient experience for the customer.
    * :red[So let us see the insights 👀.]
    """)
    # ______________________________________________________________________________________________________________________________________________________________________________________________________

if Planning :
    st.sidebar.header(":orange[About Project]")
    st.sidebar.subheader ('Data Co SMART SUPPLY CHAIN EDA 📊')
    st.sidebar.write("""
    * This is my MID Project during my Data Science Diploma @Epsilon AI. 
    * In this Project we have 4 EDAs:
        * ('Challenges🔎','Insight💡' , 'Custom EDA for User👨‍👩‍👦‍👦').
        * Also will explain a brief of :
            * Challenges
            * Insights 
            * Custom EDA for User 

    * Data Source:
        1) mendeley : https://data.mendeley.com/datasets/8gx2fvg2k6/5
        2) Kaggle : https://www.kaggle.com/datasets/shashwatwork/dataco-smart-supply-chain-for-big-data-analysis
    """)
    st.sidebar.write("""
    * Data Details:
        * 180519 Row, 53 columns
        * order_id : 65752
        * customer : 20652
        * customer_countries : 2
        * customer_segment : 3
        * customer_states : 46
        * customer_cities : 563
        * market : 5
        * order_regions : 23
        * order_countries : 164
        * order_city : 3597
        * Products : 118
        * categories : 51 
    """)
    # ______________________________________________________________________________________________________________________________________________________________________________________________________

if About_me :
    st.sidebar.header(":green[About me]")
    st.sidebar.write("""
    - Osama SAAD
    - Student : Data Scaience & Machine Learning  @Epsilon AI
    - Infor ERP (EAM/M3) key Business.User | Infor DMS, Assets and System Control Supervisor @ Ibnsina Pharma
    - LinkedIn: 
        https://www.linkedin.com/in/ossama-ahmed-saad-525785b2
    - Github : 
        https://github.com/OsamaSamnudi
    """)
# ______________________________________________________________________________________________________________________________________________________________________________________________________
# Make 4 Tabs for Challenges & Insights , Sales , Orders , Products , Customers
def NAN (df):
    return df.isna().sum().reset_index(name='NAN_Count').query('NAN_Count > 0')
# st.image("Supply Chain Logo.png")
st.title ('Data Co SMART SUPPLY CHAIN EDA 📊')
Challenges , Insight , Custom  = st.tabs(['Challenges🔎','Insight💡' , 'Custom EDA for User👨‍👩‍👦‍👦'])

with Challenges:
    with st.container():
        st.header('Challenges🔎')
        Challenges = st.checkbox(":blue[Challenges]")
        if Challenges:
            col1, col2, col3 = st.columns([7,7,7])
            with col1:
                st.write("✅date types :")
                OldDataType = Old_df.dtypes.reset_index(name='Type')
                st.dataframe(data=OldDataType, hide_index=True,use_container_width=True)
                st.write("✅Null Values :")
                st.dataframe(data=NAN(Old_df), use_container_width=True)
            with col2:
                st.write(f"✅Shape of Data  : {Old_df.shape}", use_container_width=True)
                st.write(f"✅Duplicated :{Old_df.duplicated().sum()}", use_container_width=True)
                st.write("✅32 byte Conversion : datetime64 (2), float32(12), int32(11)")
                st.write("✅Outlier_lst:")
                st.dataframe(data=Outlier_lst, use_container_width=True)

            with col3:
                st.write("""
                    * ✅Feature Engineering (New Fearures) :
                        * order_date_(year) , order_date_(month)
                        * order_date_(day)
                        * order_date_(d_n)
                        * shipping_date_(year)
                        * shipping_date_(month)
                        * shipping_date_(day)
                        * shipping_date_(d_n)
                        * days_diff(schad_vs_real)
                        * order_profit_status
                        * days_shipping(status)
                        * category_name
                        * OPS Status""" )
                st.write("""
                    * ❌ Drop Unnecessary Columns :
                        * customer_email
                        * customer_fname 
                        * customer_lname
                        * customer_password
                        * customer_street
                        * customer_zipcode
                        * order_customer_id
                        * product_category_id
                        * order_item_cardprod_id
                        * order_item_id
                        * order_item_product_price
                        * product_card_id
                        * product_description
                        * product_image""" )
            with st.container():
                st.subheader('Data Issue on Category Featrue')
                col_1, col_2, col_3 = st.columns([10,0.5,10])
                with col_1:
                    st.write("There is duplicate in category_name (Electronics) as it has two diff ids (37 , 13)")
                    Issue_Category = df[(df.category_id == 37) | (df.category_id == 13)][['category_id' , 'category_name']].value_counts().reset_index(name='count')
                    st.dataframe(data=Issue_Category, use_container_width=False)
                    Issue_Category_1 = df[(df.category_id == 37) | (df.category_id == 13)][['category_name','category_id','product_name']].value_counts().reset_index(name='count').sort_values('category_id')
                    st.dataframe(data=Issue_Category_1, use_container_width=False)
                    st.code("df[df['product_name'].str.contains(r'\w*Under Armour\w*',case=False)][['category_id','category_name','product_name']].value_counts().reset_index(name='count')")
                    st.write("""
                    * Total_All_Sales : 3,966,902.75
                    * Total_Sales_Electronic : 40,891.38 = 0.01 % from total sales
                    * Electronic_row_count:3156 , And DF_row_count: 180,519 = 0.017 %

                    - (My comment & action) : After categorization count check :
                    - There are items allocated to wrong category = "Electronic" ,
                    - After check (category vs real market data) found that (Category ID "37")  shoud be allocated to ("35 - Golf Golves").
                    - And ("Category ID 13") should be allocated to ("29 - Shop By Sports").
                    therefore with considrate keep the data as domian, created new Feature "New Cateogry" with above update to use it in our EDA.
                    """)
                with col_3:
                    st.write("Check Products sample in internet :")
                    st.image("Category issue.png")
    with st.container():
        st.subheader('Check Corrolateion')
        Corro_Box = st.checkbox(":blue[Check Corrolateion]")
        if Corro_Box:
            Corro = df[['order_id','late_delivery_risk','days_diff(schad_vs_real)','days_for_shipping_(real)','days_for_shipment_(scheduled)'
              ,'customer_id','product_price','order_item_quantity','order_item_discount_rate','order_item_discount','order_item_total'
              ,'order_item_profit_ratio', 'order_profit_per_order']].corr()
            Corr_fig = px.imshow(Corro , width=1300 , height=1300 , text_auto=True,color_continuous_scale=px.colors.colorbrewer.Spectral)
            st.plotly_chart(Corr_fig , use_container_width=True,theme="streamlit")
#________________________________________________________________________________________________________________________________________________________________________________________________________
with Insight:
    with st.container():
        st.subheader("Insight 💡 + Overall Conclusions")
        st.info("""
        * The Main Feature Analysis :
            Order Status , OPS Status , Order Profit Status , Type (Payment Method) , Market , Customer Segment , 
            Shipment Mode (Days Shipment) , Order Region , Department Name , Order/ Year/Month/Day , Late Delivery Risk
        """)
        Sales_Box = st.checkbox(":blue[Sales 💰 Insight]")
        if Sales_Box:
            with st.container():
                st.write("⚠️ 1) Profit (Gain/Loss) vs Orders Count ")
                col_001 ,col_002,col_003 = st.columns([10,1,10])
                with col_001:
                    Profit_review_year = df.groupby(['order_date_(year)','order_profit_status'])[['order_profit_per_order']].agg(sum= ('order_profit_per_order' , 'sum'),
                                         Order_Count=('order_profit_per_order','count'),
                                         Order_Count_Precentage=('order_profit_per_order' , lambda x : x.count() / len(df))).sort_values('sum',ascending = False).reset_index()
                    Summary_Profit_review_year = pd.pivot_table(Profit_review_year ,index= 'order_date_(year)' , columns='order_profit_status').reset_index()
                    Order_count = df.groupby(['order_status','order_profit_status'])[['order_id']].count().reset_index()
                    Pie_Order_count = px.pie(Order_count , names='order_profit_status' , values='order_id',title='Order in Gain/Loss').update_traces(textinfo='percent+value')
                    st.plotly_chart(Pie_Order_count , use_container_width=True,theme="streamlit")
                with col_003:
                    st.success('Check the Gain/Loss for all itmes')
                    Products_profit_details = df.groupby(['department_name' , 'category_name' , 'product_category_id' , 'product_name','order_profit_status'])[['order_profit_per_order']].agg(sum= ('order_profit_per_order' , 'sum'),
                                                                                                                                          count=('order_profit_per_order' , 'count')).sort_values('product_category_id').reset_index()
                    Products_profit_details_Update = Products_profit_details.pivot_table(index=['product_category_id','product_name','category_name'],values=['sum' , 'count'] , columns='order_profit_status').sort_values('product_category_id').reset_index()
                    MSK = Products_profit_details_Update.describe()
                    st.dataframe(data= MSK, use_container_width=False)
            with st.container():
                Data_Sample = df[['order_status','type','market','order_date_(dateorders)','order_id',
                    'product_name','product_price','order_item_quantity','order_item_discount_rate','order_item_discount','order_item_total','order_item_profit_ratio','order_profit_per_order','order_profit_status']].sample(10)
                st.dataframe(data= Data_Sample, use_container_width=False)
                Show_Code = st.checkbox(":red[Show Code]")
                if Show_Code:
                    st.code("""
                    Products_profit_details = df.groupby(['product_category_id' , 'product_name','order_profit_status'])[['order_profit_per_order']].agg(sum= ('order_profit_per_order' , 'sum'),
                                                                                                        count=('order_profit_per_order' , 'count')).sort_values('product_category_id').reset_index()
                    Products_profit_details_Update = Products_profit_details.pivot_table(index=['product_category_id','product_name','category_name'],values=['sum','count'] 
                                                                                                        ,columns='order_profit_status').sort_values('product_category_id').reset_index()
                    MSK = Products_profit_details_Update.describe()
                        """)
            st.error("""
                * By Checking Sales (Profit per order), found about 18.7 % has negative Values in (item_profit_ratio)
                  And this caused to convert the profile value to negative.
                * So we shall check by many ways to get the final observations and cuses from the possbile Data.
                  """)

            with st.container(): # Discount Check
                st.write("⚠️ 2) Profit (Gain/Loss) vs Discount ")
                Discount = df.groupby(['department_name' , 'order_profit_status'])[['order_item_discount']].sum().sort_values('order_item_discount' , ascending=False).reset_index()
                Dicount_FIG = px.histogram(Discount , x= 'department_name' , y='order_item_discount',color='order_profit_status',barmode='group',text_auto=True,title = "Total discount per Department")
                st.plotly_chart(Dicount_FIG , use_container_width=True,theme="streamlit")
                st.error('No Loss value is over than Gain After checking  Discount per Department')

            with st.container():
                st.write("⚠️ 3) Profit (Gain/Loss) vs Order Status")
                col_0_0, col_0_1, col_0_2 = st.columns([10,0.1,10])
                with col_0_0:
                    msk = df.groupby(['order_status','order_date_(year)'])[['order_id']].count().sort_values('order_id').reset_index()
                    fig = px.histogram(msk , x='order_date_(year)' , y='order_id' , color='order_status',barmode='group',text_auto=True , title ='Check order_status per Year')
                    st.plotly_chart(fig , use_container_width=True,theme="streamlit")
                with col_0_2:
                    msk = df.groupby(['OPS Status','order_date_(year)'])[['order_id']].count().sort_values('order_id').reset_index()
                    fig = px.histogram(msk , x='order_date_(year)' , y='order_id' , color='OPS Status',barmode='group',text_auto=True , title ='Check OPS per Year')
                    st.plotly_chart(fig , use_container_width=True,theme="streamlit")
                st.error("Not Logic to have Pending Transactions from past years, But may this Observation indicates for the way of collecting this data, and may have been got by end of every year.")
            with st.container():
                S_col_1, S_col_2, S_col_3 = st.columns([10,0.1,10])
                with S_col_1:
                    st.dataframe(data=Profit_review_year, use_container_width=True)
                with S_col_3:
                    st.dataframe(data=Summary_Profit_review_year, use_container_width=True)
                    
            with st.container():
                S_col_4, S_col_5, S_col_6 = st.columns([10,0.1,10])
                with S_col_4:
                    All_Sales_Per_Year = df.groupby(['order_date_(year)' , 'order_profit_status'])[['order_profit_per_order']].sum().sort_values(['order_profit_per_order'],ascending=False).reset_index()
                    Fig_All_Sales_Year = px.histogram(All_Sales_Per_Year , x='order_date_(year)' ,
                                          y='order_profit_per_order',color='order_profit_status',
                                          barmode='group',text_auto=True , title='Profit Status and values per Year')
                    st.plotly_chart(Fig_All_Sales_Year , use_container_width=True,theme="streamlit")
                with S_col_6:
                    Net_Loss_gain = df.groupby(['order_profit_status','OPS Status'])[['order_profit_per_order']].sum().sort_values('order_profit_per_order' , ascending=False).reset_index()
                    Fig_Net_Loss_gain = px.histogram(Net_Loss_gain , x='OPS Status' , y='order_profit_per_order' , color='order_profit_status',text_auto=True,width=1000 ,height=600 , title = 'Gain / Loss per Order Status (New Feature)')
                    st.plotly_chart(Fig_Net_Loss_gain , use_container_width=True,theme="streamlit")
                st.error("Loss Values Distributing for every year with (Strange Balance😳), it look like a target need to reach.")
            with st.container():
                def Profit_insight (data):
                    msk = df.groupby([data,'order_profit_status'])[['order_profit_per_order']].agg(sum= ('order_profit_per_order' , 'sum'),
                             Order_Count=('order_profit_per_order','count'),
                             Order_Count_Precentage=('order_profit_per_order' , lambda x : x.count() / len(df))).sort_values([data,'order_profit_status'],ascending = True).reset_index()
                    return pd.pivot_table(msk ,index= data , columns='order_profit_status',aggfunc='sum').reset_index()  
            
                st.write('* Check the (Type) Feature :')
                S_col_7, S_col_8, S_col_9 = st.columns([10,0.1,10])
                VAR = 'type'
                with S_col_7:
                    st.write(f"✅1) {VAR} vs order_profit_status in order_profit_per_order")
                    st.dataframe(data=Profit_insight(VAR), use_container_width=True)
                with S_col_9:
                    Sales_Type = df.groupby(['order_profit_status',VAR])[['order_profit_per_order']].sum().reset_index().sort_values('order_profit_per_order' , ascending=False)
                    Fig_Sales_Type = px.histogram(Sales_Type , x = 'order_profit_status' , y='order_profit_per_order' , color = VAR , width=1000 , height=600 ,barmode='group', text_auto=True ,title=f'Profit per {VAR}')
                    st.plotly_chart(Fig_Sales_Type , use_container_width=True,theme="streamlit")

            with st.container():
                S_col_10, S_col_11, S_col_12 = st.columns([10,0.1,10])
                VAR = 'market'
                with S_col_10:
                    st.write(f"✅2) {VAR} vs order_profit_status in order_profit_per_order")
                    st.dataframe(data=Profit_insight(VAR), use_container_width=True)
                    st.info("""
                        Note :
                        * LATAM is a Spanish acronym that stands for Latin America.
                        * It is commonly used to refer to the region of the Americas that is south of the United States, including Mexico, Central America, South America.
                        """)
                with S_col_12:
                    Sales_market = df.groupby(['order_profit_status',VAR])[['order_profit_per_order']].sum().reset_index().sort_values('order_profit_per_order' , ascending=False)
                    Fig_Sales_market = px.histogram(Sales_market , x = 'order_profit_status' , y='order_profit_per_order' , color = VAR , width=1000 , height=600 ,barmode='group', text_auto=True ,title=f'Profit per {VAR}')
                    st.plotly_chart(Fig_Sales_market , use_container_width=True,theme="streamlit")


            with st.container():
                S_col_13, S_col_14, S_col_15 = st.columns([10,0.1,10])
                VAR = 'customer_segment'
                with S_col_13:
                    st.write(f"✅3) {VAR} vs order_profit_status in order_profit_per_order")
                    st.dataframe(data=Profit_insight(VAR), use_container_width=True)
                with S_col_15:
                    MSK = df.groupby(['order_profit_status',VAR])[['order_profit_per_order']].sum().reset_index().sort_values('order_profit_per_order' , ascending=False)
                    Fig_MSK = px.histogram(MSK , x = 'order_profit_status' , y='order_profit_per_order' , color = VAR , width=1000 , height=600 ,barmode='group', text_auto=True ,title=f'Profit per {VAR}')
                    st.plotly_chart(Fig_MSK , use_container_width=True,theme="streamlit")    
                    
            with st.container():
                S_col_16, S_col_17, S_col_18 = st.columns([10,0.1,10])
                VAR = 'shipping_mode'
                with S_col_16:
                    st.write(f"✅4) {VAR} vs order_profit_status in order_profit_per_order")
                    st.dataframe(data=Profit_insight(VAR), use_container_width=True)
                with S_col_18:
                    MSK = df.groupby(['order_profit_status',VAR])[['order_profit_per_order']].sum().reset_index().sort_values('order_profit_per_order' , ascending=False)
                    Fig_MSK = px.histogram(MSK , x = 'order_profit_status' , y='order_profit_per_order' , color = VAR , width=1000 , height=600 ,barmode='group', text_auto=True ,title=f'Profit per {VAR}')
                    st.plotly_chart(Fig_MSK , use_container_width=True,theme="streamlit")

            with st.container():
                S_col_19, S_col_20, S_col_21 = st.columns([10,0.1,10])
                VAR = 'days_shipping(status)'
                with S_col_19:
                    st.write(f"✅5) {VAR} vs order_profit_status in order_profit_per_order")
                    st.dataframe(data=Profit_insight(VAR), use_container_width=True)
                with S_col_21:
                    # Var_1 = 'days_shipping(status)'
                    MSK = df.groupby(['order_profit_status',VAR])[['order_profit_per_order']].sum().reset_index().sort_values('order_profit_per_order' , ascending=False)
                    Fig_MSK = px.histogram(MSK , x = 'order_profit_status' , y='order_profit_per_order' , color = VAR , width=1000 , height=600 ,barmode='group', text_auto=True ,title=f'Profit per {VAR}')
                    st.plotly_chart(Fig_MSK , use_container_width=True,theme="streamlit")
                    
            with st.container():
                S_col_22, S_col_23, S_col_24 = st.columns([10,0.1,10])
                VAR = 'order_region'
                with S_col_22:
                    st.write(f"✅6) {VAR} vs order_profit_status in order_profit_per_order")
                    st.dataframe(data=Profit_insight(VAR), use_container_width=True)
                with S_col_24:
                    MSK = df.groupby(['order_profit_status',VAR])[['order_profit_per_order']].sum().reset_index().sort_values('order_profit_per_order' , ascending=False)
                    Fig_MSK = px.histogram(MSK , x = 'order_profit_status' , y='order_profit_per_order' , color = VAR , width=1000 , height=600 ,barmode='group', text_auto=True ,title=f'Profit per {VAR}')
                    st.plotly_chart(Fig_MSK , use_container_width=True,theme="streamlit")

            with st.container():
                S_col_25, S_col_26, S_col_27 = st.columns([10,0.1,10])
                VAR = 'department_name'
                with S_col_25:
                    st.write(f"✅7) {VAR} vs order_profit_status in order_profit_per_order")
                    st.dataframe(data=Profit_insight(VAR), use_container_width=True)
                with S_col_27:
                    MSK = df.groupby(['order_profit_status',VAR])[['order_profit_per_order']].sum().reset_index().sort_values('order_profit_per_order' , ascending=False)
                    Fig_MSK = px.histogram(MSK , x = 'order_profit_status' , y='order_profit_per_order' , color = VAR , width=1000 , height=600 ,barmode='group', text_auto=True ,title=f'Profit per {VAR}')
                    st.plotly_chart(Fig_MSK , use_container_width=True,theme="streamlit")     
                    
            with st.container():
                VAR = 'Total Gain/Loss'
                st.write(f"✅8) {VAR} vs order_profit_status in order_profit_per_order")
                MSK = df.groupby(['order_profit_status'])[['order_profit_per_order']].sum().sort_values('order_profit_status').reset_index()
                Fig_MSK = px.histogram(MSK , x='order_profit_status' , y='order_profit_per_order' , color='order_profit_status',barmode='group',text_auto=True,width=600, height=400)
                st.plotly_chart(Fig_MSK , use_container_width=True,theme="streamlit")
                st.error("About 48% is Loss and it is big value and no feature to clarify the cost type dusting the process (order,shipping,operations,etc...)")
                
                line = df.groupby(['order_date_(year)','order_date_(month)'])[['order_profit_per_order']].sum().sort_values(['order_date_(year)','order_date_(month)']).reset_index()
                Fig_Line = px.line(line , x = 'order_date_(month)' , y='order_profit_per_order' , color='order_date_(year)',title='Profit per year (Order Date)')
                st.plotly_chart(Fig_Line , use_container_width=True,theme="streamlit")

                line_s = df.groupby(['shipping_date_(year)','shipping_date_(month)'])[['order_profit_per_order']].sum().sort_values(['shipping_date_(year)','shipping_date_(month)']).reset_index()
                Fig_Line_s = px.line(line_s , x = 'shipping_date_(month)' , y='order_profit_per_order' , color='shipping_date_(year)',title='Profit per year (Shipment Date)')
                st.plotly_chart(Fig_Line_s , use_container_width=True,theme="streamlit")
                st.subheader("🔚 Conclusions on Sales :")
                st.write("""
                *  By Checking Sales found about 18.7 % has Negative Values in (item_profit_ratio) and this caused to convert the profile value to negative.
                *  So we compared the new Features (Profit per order)/(OPS Status)/(order_profit_status) and (order_profit_per_order) vs Every effective Feature:
                *  Found that the distribution of Loss is Over years no in spacifice Feature.
                *  Year: Found that the distribution of Loss is Over years no in specific year (Gain 24% : 28%) and (Loss 5% : 6%) overall years.
                *  OPS Status : The same with this Feature that indicates The order/Payment Completion Status.
                    *  The Completed is the top then Under Process, which indicates for Good Progress.
                       But once view in deep for the details of OPS Status the new feature of "order_status" found "Pending Orders/Payments" in every year, which indicates for wrong details,
                       or the data got in a spacific time around these years.
                *  Type : Debit Payment method is the most used then Transfer , which indicates that the most customers have deals with this company.
                *  Market : Europe and Latam are the most Market in data contrary to USA, Africa.
                *  Customer Segment : Consumer is the top (42% - 4M).
                *  Shipping_mode : Stander Class is the Top (48% - 4.7M).
                *  days_shipping(status) : Most of status is late (46% - 4.4M).
                *  order_region : Western Europe is the top (12% - 1.2M).
                *  department_name (Product Class) : Fan Shop is the top (30% - 3.6M) , Book Shop is less (0,0018% - 2604).
                * 🔚 Finally :
                    *  The Negative values is one from below :
                        *  Wrong Data , Should recalculate the Profit again and is this case the profit will be "11M" instated of "7M".
                        *  True Data , and in this case should know the reason as no feature is indicate the cost for every step (Operations, Orders, Shipping)
                    * About 48% is Loss so if considerate that the data is True, we have focus for "Late" orders to reduce it.
                      Western Europe is the top region, may the shipment cost the cause for the loss.
                    * Profit in all Years (2015 to 07/2017) likely same, but a drop happened starting form 08/2017 and it is expected reaction for the “Late” Comment.
                    * No Addition details for cost type to clarify the reason on negative ratio percentage.
                """)
#________________________________________________________________________________________________________________________________________________________________________________________________________
    with st.container():
        Customers_Box = st.checkbox(":blue[Customers👨‍👩‍👦‍👦Insight]")
        if Customers_Box:
            st.subheader('Customers👨‍👩‍👦‍👦Insight')
            with st.container():
                st.success("5 Samples from Customers_Master DF")
                Customers_Master = df.groupby(['customer_id' , 'customer_country' , 'customer_segment']).agg({'order_id' : 'count' , 'order_profit_per_order':'sum'}).sort_values('customer_id').reset_index()
                Customers_Master['Profit_Status'] = Customers_Master['order_profit_per_order'].apply(lambda x : "Positive" if x > 1 else "Negative") # Categorization Profit Value
                Customers_Master.columns = ['customer_id','customer_country','customer_segment','total_orders','total_orders_profit','Profit_Status']
                st.dataframe(data=Customers_Master.sample(5), use_container_width=False)
                M_Col_1, M_Col_2 , M_Col_3 = st.columns([10,10,10])
                with M_Col_1:
                    VAR = 'Total Customer in Country'
                    Customers_Data = df.groupby(['customer_id' , 'customer_country' , 'customer_segment' ]).agg({'order_id' : 'count' , 'order_profit_per_order':'sum'}).sort_values('customer_id').reset_index()
                    Total_Customers = Customers_Data.groupby(['customer_country'])[['customer_id']].count().reset_index()
                    Cust_fig = px.pie(Total_Customers , names='customer_country' , values='customer_id',title=f"✅1) {VAR} ").update_traces(textinfo='percent+value')
                    st.plotly_chart(Cust_fig , use_container_width=True,theme="streamlit")
                with M_Col_2:
                    VAR = 'Total Customer in Segment'
                    Customers_Data = df.groupby(['customer_id' , 'customer_country' , 'customer_segment' ]).agg({'order_id' : 'count' , 'order_profit_per_order':'sum'}).sort_values('customer_id').reset_index()
                    Total_Customers = Customers_Data.groupby(['customer_segment'])[['customer_id']].count().reset_index()
                    Cust_fig = px.pie(Total_Customers , names='customer_segment' , values='customer_id',title=f"✅2) {VAR} ").update_traces(textinfo='percent+value')
                    st.plotly_chart(Cust_fig , use_container_width=True,theme="streamlit")
                with M_Col_3:
                    VAR = 'Orders Count per Customer_country'
                    Customers_Data = df.groupby(['customer_id' , 'customer_country' , 'customer_segment' ]).agg({'order_id' : 'count' , 'order_profit_per_order':'sum'}).sort_values('customer_id').reset_index()
                    Cust_fig_1 = px.pie(Customers_Data , names='customer_country' , values='order_id',width=500 , height=500,title=f"✅3) Customers {VAR} ").update_traces(textinfo='percent+value')
                    st.plotly_chart(Cust_fig_1 , use_container_width=True,theme="streamlit")    
                    
            with st.container():
                C_Col_1, C_Col_2 , C_Col_3 = st.columns([10,10,10])
                with C_Col_1:
                    VAR = 'Customer_country in order_profit'
                    Customers_Data = df.groupby(['customer_id' , 'customer_country' , 'customer_segment' ]).agg({'order_id' : 'count' , 'order_profit_per_order':'sum'}).sort_values('customer_id').reset_index()
                    Cust_fig_3 = px.pie(Customers_Data , names='customer_country' , values='order_profit_per_order',width=500 , height=500,title=f"✅4) {VAR} ").update_traces(textinfo='percent+value')
                    st.plotly_chart(Cust_fig_3 , use_container_width=True,theme="streamlit")
                with C_Col_2:
                    VAR = 'Orders Count per Customer_segment'
                    Customers_Data = df.groupby(['customer_id' , 'customer_country' , 'customer_segment' ]).agg({'order_id' : 'count' , 'order_profit_per_order':'sum'}).sort_values('customer_id').reset_index()
                    Cust_fig_2 = px.pie(Customers_Data , names='customer_segment' , values='order_id',width=500 , height=500,title=f"✅5) {VAR} ").update_traces(textinfo='percent+value')
                    st.plotly_chart(Cust_fig_2 , use_container_width=True,theme="streamlit")                    
                with C_Col_3:
                    VAR = 'Customer_segment in order_profit'
                    Customers_Data = df.groupby(['customer_id' , 'customer_country' , 'customer_segment' ]).agg({'order_id' : 'count' , 'order_profit_per_order':'sum'}).sort_values('customer_id').reset_index()
                    Cust_fig_4 = px.pie(Customers_Data , names='customer_segment' , values='order_profit_per_order',width=500 , height=500,title=f"✅6) {VAR} ").update_traces(textinfo='percent+value')
                    st.plotly_chart(Cust_fig_4 , use_container_width=True,theme="streamlit")

            with st.container():
                C_Col_7, C_Col_8 , C_Col_9 = st.columns([10,10,10])
                Customers_Data['customer_id'] = Customers_Data['customer_id'].astype(str)
                Customers_Master = df.groupby(['customer_id' , 'customer_country' , 'customer_segment']).agg({'order_id' : 'count' , 'order_profit_per_order':'sum'}).sort_values('customer_id').reset_index()
                Customers_Master['Profit_Status'] = Customers_Data['order_profit_per_order'].apply(lambda x : "Positive" if x > 1 else "Negative") # Categorization Profit Value
                Customers_Master.columns = ['customer_id','customer_country','customer_segment','total_orders','total_orders_profit','Profit_Status']
                with C_Col_7:
                    VAR = 'customer_country vs total_orders'
                    Cust_fig_5 = px.histogram(Customers_Master , x='customer_country',y='total_orders' , color = 'Profit_Status',barmode='group' , text_auto=True,title=f"✅7) {VAR} (With Possitve/Negative Flag) ")
                    st.plotly_chart(Cust_fig_5 , use_container_width=True,theme="streamlit")
                with C_Col_8:
                    VAR = 'Customer_segment in order_profit'
                    Customers_Data = df.groupby(['customer_id' , 'customer_country' , 'customer_segment' ]).agg({'order_id' : 'count' , 'order_profit_per_order':'sum'}).sort_values('customer_id').reset_index()
                    Cust_fig_6 = px.histogram(Customers_Master,x='customer_country',y='total_orders',color='customer_segment',barmode='group',text_auto=True,title=f"✅8) {VAR}")
                    st.plotly_chart(Cust_fig_6 , use_container_width=True,theme="streamlit")
                with C_Col_9:
                    VAR = 'Customer_segment in order_profit'
                    Customers_Data = df.groupby(['customer_id' , 'customer_country' , 'customer_segment' ]).agg({'order_id' : 'count' , 'order_profit_per_order':'sum'}).sort_values('customer_id').reset_index()
                    Cust_fig_7 = px.histogram(Customers_Master,x='customer_country',y='total_orders',color='customer_segment',barmode='group',text_auto=True,title=f"✅9) {VAR} ")
                    st.plotly_chart(Cust_fig_7 , use_container_width=True,theme="streamlit") 
                    
            with st.container():
                st.write("✅10) Customer Longitude & Latitude corresponding to location of store")
                import pandas as pd
                import numpy as np
                import streamlit as st
                test = df[['latitude','longitude']]
                st.map(test)
                
            with st.container():
                st.error("""
                    * Note:
                        * EE UU is the Spanish abbreviation for Estados Unidos, which means United States of America.
                        * Puerto Rico is located in the Caribbean Sea, and it has a population of over 3 million people. The official languages of Puerto Rico are Spanish and English.
                        * Consumers are the final users of goods or services. They are the people who purchase and use products for their own needs.
                    * 61% of Customers from “Puerto Rico” (12k Customers) and the rest from USA (Central of USA as next EDAs), take 61% from the Orders (111k orders) with 52% from total Profit (2M).
                    * 51% of Customers are “Consumers” (10k Customers).""")
#________________________________________________________________________________________________________________________________________________________________________________________________________
    with st.container():
        Orders_Products_Box = st.checkbox(":blue[Products 📦 & Orders📝]")
        if Orders_Products_Box:
            st.subheader('Products Over view')
            All_Products = df[['department_name', 'new_category_name','product_name']].drop_duplicates().reset_index(drop=True)
            Cat = df[['department_name','new_category_name']].drop_duplicates().sort_values(['department_name' , 'new_category_name']).reset_index(drop=True)
            Pro = All_Products.groupby('new_category_name')['product_name'].count().sort_values(ascending=False).reset_index()
            All_Products = pd.merge(how='inner', left = Cat , right=Pro)
            All_Products = All_Products.sort_values('product_name' , ascending=False).reset_index(drop=True)
            Fig = px.histogram(All_Products , x='new_category_name' , y='product_name' , color='department_name', text_auto=True,title = '⚠️ 1) Products Count per category')
            st.plotly_chart(Fig , use_container_width=True,theme="streamlit")
            Fig = px.histogram(All_Products , x='department_name' , y='product_name' , color='department_name', text_auto=True,title = '⚠️ 2) Products Count per Department')
            st.plotly_chart(Fig , use_container_width=True,theme="streamlit")
            st.info("""
            * “Golf”, “Kids Golf”, “Shop by Sports” and all sports categories are have the most products.
            * Also “Outdoors” Department has the most products.
            """)
            
            with st.container():
                st.subheader('Orders')
                O_col_1, S_col_2, S_col_3 = st.columns([10,0.1,10])
                with O_col_1:
                    VAR = 'type'
                    MSK = df.groupby(['days_shipping(status)',VAR])[['order_id']].count().reset_index().sort_values('order_id' , ascending=False)
                    Fig_MSK = px.histogram(MSK , x = 'days_shipping(status)' , y='order_id' , color = VAR , width=1000 , height=600 ,barmode='group', text_auto=True ,title=f"✅1) Orders Count in days_shipping(status) with {VAR}")
                    st.plotly_chart(Fig_MSK , use_container_width=True,theme="streamlit")
                with S_col_3:
                    VAR_1 = 'market'
                    MSK = df.groupby(['days_shipping(status)',VAR_1])[['order_id']].count().reset_index().sort_values('order_id' , ascending=False)
                    Fig_MSK = px.histogram(MSK , x = 'days_shipping(status)' , y='order_id' , color = VAR_1 , width=1000 , height=600 ,barmode='group', text_auto=True ,title=f"✅2) Orders Count in days_shipping(status) with {VAR_1}")
                    st.plotly_chart(Fig_MSK , use_container_width=True,theme="streamlit")

            with st.container():
                O_col_4, S_col_5, S_col_6 = st.columns([10,0.1,10])
                with O_col_4:
                    VAR = 'customer_segment'
                    MSK = df.groupby(['days_shipping(status)',VAR])[['order_id']].count().reset_index().sort_values('order_id' , ascending=False)
                    Fig_MSK = px.histogram(MSK , x = 'days_shipping(status)' , y='order_id' , color = VAR , width=1000 , height=600 ,barmode='group', text_auto=True ,title=f"✅3) Orders Count in days_shipping(status) with {VAR}")
                    st.plotly_chart(Fig_MSK , use_container_width=True,theme="streamlit")
                with S_col_6:
                    VAR_1 = 'shipping_mode'
                    MSK = df.groupby(['days_shipping(status)',VAR_1])[['order_id']].count().reset_index().sort_values('order_id' , ascending=False)
                    Fig_MSK = px.histogram(MSK , x = 'days_shipping(status)' , y='order_id' , color = VAR_1 , width=1000 , height=600 ,barmode='group', text_auto=True ,title=f"✅4) Orders Count in days_shipping(status) with {VAR_1}")
                    st.plotly_chart(Fig_MSK , use_container_width=True,theme="streamlit")
                        
            with st.container():
                O_col_7, S_col_8, S_col_9 = st.columns([10,0.1,10])
                with O_col_7:
                    VAR = 'customer_country'
                    MSK = df.groupby(['days_shipping(status)',VAR])[['order_id']].count().reset_index().sort_values('order_id' , ascending=False)
                    Fig_MSK = px.histogram(MSK , x = 'days_shipping(status)' , y='order_id' , color = VAR , width=1000 , height=600 ,barmode='group', text_auto=True ,title=f"✅5) Orders Count in days_shipping(status) with {VAR}")
                    st.plotly_chart(Fig_MSK , use_container_width=True,theme="streamlit")
                with S_col_9:
                    VAR_1 = 'order_region'
                    MSK = df.groupby(['days_shipping(status)',VAR_1])[['order_id']].count().reset_index().sort_values('order_id' , ascending=False)
                    Fig_MSK = px.histogram(MSK , x = 'days_shipping(status)' , y='order_id' , color = VAR_1 , width=1000 , height=600 ,barmode='group', text_auto=True ,title=f"✅6) Orders Count in days_shipping(status) with {VAR_1}")
                    st.plotly_chart(Fig_MSK , use_container_width=True,theme="streamlit")
                        
            with st.container():
                VAR_1 = 'customer_country'
                MSK = df.groupby(['order_region',VAR_1])[['order_id']].count().reset_index().sort_values('order_id' , ascending=False)
                Fig_MSK = px.histogram(MSK , x = 'order_region' , y='order_id' , color = VAR_1 , width=1000 , height=600 ,barmode='group', text_auto=True ,title=f"✅7) Orders Count in days_shipping(status) with {VAR_1}")
                st.plotly_chart(Fig_MSK , use_container_width=True,theme="streamlit")
            with st.container():
                st.error("""
                * Note:
                    * EE UU is the Spanish abbreviation for Estados Unidos, which means United States of America.
                    * Puerto Rico is located in the Caribbean Sea, and it has a population of over 3 million people. The official languages of Puerto Rico are Spanish and English.
                * Most “Late” orders in “Latin America (LATAM)” then “Europe” then “Asia”, which indicates for the far orders are the most and the most of them are “Late”!.
                * The same in “Type (Payment Method)”, the higher orders count in “Late/Debit” (39k) and the “Early/Debit” was (16k), which indicates the most of customers in “Deal Contract Mode”.
                * High Orders count in “Consumer” Customer type and the most count in “Late” Status! (The same in Sales EDA).
                * By comparing “Customer Country ()” vs “Order Region ()” found that all orders are from Two Countries (EE.UU (USA) and Puerto Rico) to higher Order Count Countries (Central of USA, Europe, Asia) and most of them in Order “Late” Status.
                on the basis of  above; Company Should review the Current Operations, Solutions in Goods Transfer to improve it, Or Study to Open Market in the most Regions/Countries to save the shipping cost and to avoid the big count of “Late” also to build/preserve the “Customer Loyalty”.
                """)

            with st.container():
                VAR_1 = 'department_name'
                MSK = df.groupby(['days_shipping(status)',VAR_1])[['order_id']].count().reset_index().sort_values('order_id' , ascending=False)
                Fig_MSK = px.histogram(MSK , x = 'days_shipping(status)' , y='order_id' , color = VAR_1 , width=1000 , height=600 ,barmode='group', text_auto=True ,title=f"✅8) Orders Count in days_shipping(status) with {VAR_1}")
                st.plotly_chart(Fig_MSK , use_container_width=True,theme="streamlit")
                
            with st.container():
                O_col_10, S_col_11, S_col_12 = st.columns([10,0.1,10])
                with O_col_10:
                    VAR = 'order_date_(year)'
                    MSK = df.groupby(['days_shipping(status)',VAR])[['order_id']].count().reset_index().sort_values('order_id' , ascending=False)
                    Fig_MSK = px.histogram(MSK , x = 'days_shipping(status)' , y='order_id' , color = VAR , width=1000 , height=600 ,barmode='group', text_auto=True ,title=f"✅9) Orders Count in days_shipping(status) with {VAR}")
                    st.plotly_chart(Fig_MSK , use_container_width=True,theme="streamlit")
                    
                with S_col_12:
                    VAR_1 = 'order_date_(month)'
                    MSK = df.groupby(['days_shipping(status)',VAR_1])[['order_id']].count().reset_index().sort_values('order_id' , ascending=False)
                    Fig_MSK = px.histogram(MSK , x = 'days_shipping(status)' , y='order_id' , color = VAR_1 , width=1000 , height=600 ,barmode='group', text_auto=True ,title=f"✅10) Orders Count in days_shipping(status) with {VAR_1}")
                    st.plotly_chart(Fig_MSK , use_container_width=True,theme="streamlit")
            with st.container():
                st.error("""
                * Note:
                    * Fan shop is a store that sells merchandise related to a particular sports team, music group, or other entity. Fan shops typically sell a variety of items, such as clothing, hats, jerseys, souvenirs, and other collectibles.
                    * Apparel is clothing or other items worn on the body. It can include items such as shirts, pants, shoes, hats, and accessories. Apparel is used to protect the body from the elements, to express personal style, and to identify with different groups or cultures.
                * “Fan Shop”, “Apparel” then “Golf” which indicated the “Customer Interesting’s” or maybe clarify the “Company specialization”.
                * By Checking the “Shipping Days Status” per “Years/Months” found that the “Late” is the Most Status. 
                """)
            with st.container():
                VAR = 'order_date_(year)'
                MSK = df.groupby(['order_date_(year)','order_date_(month)'])[['order_id']].count().sort_values(['order_date_(year)','order_date_(month)']).reset_index()
                Fig_MSK = px.line(MSK , x = 'order_date_(month)' , y='order_id' , color='order_date_(year)',title=f"✅11) Orders Count Time Series Per {VAR}")
                st.plotly_chart(Fig_MSK , use_container_width=True,theme="streamlit")
            with st.container():
                VAR = 'shipping_date_(year)'
                MSK = df.groupby(['shipping_date_(year)','shipping_date_(month)'])[['order_id']].count().sort_values(['shipping_date_(year)','shipping_date_(month)']).reset_index()
                Fig_MSK = px.line(MSK , x = 'shipping_date_(month)' , y='order_id' , color='shipping_date_(year)',title=f"✅12) Orders Count Time Series Per {VAR}")
                st.plotly_chart(Fig_MSK , use_container_width=True,theme="streamlit")
                
            with st.container():
                S_col_00, S_col_01, S_col_02 = st.columns([10,1,10])
                with S_col_00:
                    VAR = 'late_delivery_risk'
                    MSK = df.groupby(['late_delivery_risk' , 'order_profit_status'])[['order_id']].count().reset_index()
                    Fig_MSK = px.histogram(MSK,x= 'late_delivery_risk',y='order_id',color= 'order_profit_status',barmode='group',text_auto=True,title=f"✅13) Orders Count in {VAR} With order_profit_status")
                    st.plotly_chart(Fig_MSK , use_container_width=True,theme="streamlit")
                    st.info('Late_delivery_risk: Categorical variable that indicates if sending is late (1), it is not late (0)')
                with S_col_02:
                    VAR = 'days_shipping(status)'
                    MSK = df.groupby(['days_shipping(status)' , 'order_profit_status'])[['order_id']].count().reset_index()
                    Fig_MSK = px.histogram(MSK,x= 'days_shipping(status)',y='order_id',color= 'order_profit_status',barmode='group',text_auto=True,title=f"✅14) Orders Count in {VAR} With order_profit_status")
                    st.plotly_chart(Fig_MSK , use_container_width=True,theme="streamlit")
                    st.info('days_shipping(status): New Categorical variable that indicates diffrent between days_diff(schad_vs_real)')
                    st.code("""
                    def lating (data):
                        if data == 0:
                            return "Timely"
                        elif data > 0:
                            return "Early"
                        else:
                            return "Late"
                    df['days_shipping(status)'] = df['days_diff(schad_vs_real)'].apply(lating)
                    """)

            with st.container():
                O_col_13, S_col_14, S_col_15 = st.columns([10,0.1,10])
                with O_col_13:
                    VAR = 'new_category_name'
                    MSK = df.groupby(['new_category_name' , 'order_profit_status'])[['order_id']].count().nlargest(10 , 'order_id').reset_index()
                    Fig_MSK = px.histogram(MSK , x= 'new_category_name' , y='order_id' ,color= 'order_profit_status',barmode='group',text_auto=True,title=f"✅15) (Total Orders) Top 10 {VAR} With order_profit_status")
                    st.plotly_chart(Fig_MSK , use_container_width=True,theme="streamlit")
                with S_col_15:
                    VAR = 'new_category_name'
                    MSK = df.groupby(['new_category_name' , 'order_profit_status'])[['order_id']].count().nsmallest(10 , 'order_id').reset_index()
                    Fig_MSK = px.histogram(MSK , x= 'new_category_name' , y='order_id' ,color= 'order_profit_status',barmode='group',text_auto=True,title=f"✅16) (Total Orders) Smallest 10 {VAR} With order_profit_status")
                    st.plotly_chart(Fig_MSK , use_container_width=True,theme="streamlit")
            with st.container():
                st.error("""
                * Note:
                    * Late_delivery_risk: Categorical variable that indicates if sending is late (1), it is not late (0)
                * Order Counts in all Years (2015 to 08/2017) likely same, but a continuous drop/retreat happened starting form 08/2017 it is expected reaction for the “Late” Comment as same one Profit.
                * “Late” behavior is dominating for all orders comparing with all available Features.
                """)
     

            
#________________________________________________________________________________________________________________________________________________________________________________________________________
with Custom:
    with st.container():
        st.subheader('Custom multivariate EDA')
        X_lst = ['Select' , 'customer_state','product_name','new_category_name','order_region','order_country','department_name','order_status','market','OPS Status','delivery_status','shipping_mode','type','days_shipping(status)','customer_segment','order_profit_status','customer_country','shipping_date_(year)','shipping_date_(month)','shipping_date_(day)','order_date_(year)','order_date_(month)','order_date_(day)']
        Y_lst = ['Select' , 'order_item_quantity','order_profit_per_order','order_item_total','order_item_discount','order_item_profit_ratio','order_item_discount_rate','product_price','days_for_shipping_(real)','days_diff(schad_vs_real)']
        Color_lst = ['Select' , 'department_name','order_status','market','OPS Status','delivery_status','shipping_mode','type','days_shipping(status)','customer_segment','order_profit_status','customer_country','shipping_date_(year)','shipping_date_(month)','shipping_date_(day)','order_date_(year)','order_date_(month)','order_date_(day)','order_date_(dateorders)','shipping_date_(dateorders)']
        Time_lst = ['Select' , 'shipping_date_(year)','shipping_date_(month)','shipping_date_(day)','order_date_(year)','order_date_(month)','order_date_(day)','order_date_(dateorders)','shipping_date_(dateorders)']
        col_1 , col_2 , col_3 = st.columns([10,10,10])
        with col_1:
            x = st.selectbox ('Select X :' , X_lst)
        with col_2:
            y = st.selectbox ('Select Y :' , Y_lst)
        with col_3:
            color = st.selectbox ('Select Color :' , Color_lst)
        Method = st.radio('Calculation Method' , ['mean' , 'sum'], horizontal=True)
        if x == 'Select' or y =='Select' or  color=='Select':
            st.write(":red[Please Select a value from every list x , y , color]")
            # st.write(":red[Please Choise a column from x & y & color:]")
        else:
            if Method == 'mean':
                MSK_AVG = df.groupby([x,color])[[y]].mean().sort_values(y).reset_index()
                FI_AVG = px.histogram(MSK_AVG , x=x , y=y , color=color,barmode='group',text_auto=True,title= f'{Method} of {x} vs {y}')
                st.plotly_chart(FI_AVG , use_container_width=True,theme="streamlit") 
            else:
                MSK_SUM = df.groupby([x,color])[[y]].sum().sort_values(y).reset_index()
                FI_SUM = px.histogram(MSK_SUM , x=x , y=y , color=color,barmode='group',text_auto=True,title= f'{Method} of {x} vs {y}')
                st.plotly_chart(FI_SUM , use_container_width=True,theme="streamlit") 
    # Line
    with st.container():
        st.subheader("Custom Time Series EDA (Line)")
        X_Line_lst = ['Select' , 'shipping_date_(year)','shipping_date_(month)','shipping_date_(day)','order_date_(year)','order_date_(month)','order_date_(day)']
        Y_Line_lst = ['Select' , 'order_item_quantity','order_profit_per_order','order_item_total','order_item_discount','order_item_profit_ratio','order_item_discount_rate',
                 'product_price','days_for_shipping_(real)','days_diff(schad_vs_real)']
        Color_Line_lst = ['Select' , 'department_name','order_status','market','OPS Status','delivery_status','shipping_mode','type','days_shipping(status)',
                     'customer_segment','order_profit_status','customer_country','shipping_date_(year)','shipping_date_(month)','shipping_date_(day)',
                     'order_date_(year)','order_date_(month)','order_date_(day)','order_date_(dateorders)','shipping_date_(dateorders)']
        col_4 , col_5 , col_6 = st.columns([10,10,10])
        with col_4:
            X = st.selectbox ('Select Line X :' , X_Line_lst)
        with col_5:
            Y = st.selectbox ('Select Line Y :' , Y_Line_lst)
        with col_6:
            COLOR = st.selectbox ('Select Line Color :' , Color_Line_lst)
        Line_Method = st.radio('Calculation Line Method' , ['mean' , 'sum'], horizontal=True)
        if X == 'Select' or Y =='Select' or  COLOR=='Select':
            st.write(":red[Please Select a value from every list x , y , color]")
        else:
            if Line_Method == 'mean':
                MSK_AVG = df.groupby([X,COLOR])[[Y]].mean().sort_values(X).reset_index()
                FI_AVG = px.line(MSK_AVG , x=X , y=Y , color=COLOR ,title= f'{Method} of {X} vs {Y} colored by {COLOR}')
                st.plotly_chart(FI_AVG , use_container_width=True,theme="streamlit") 
            else:
                MSK_SUM = df.groupby([X,COLOR])[[Y]].sum().sort_values(X).reset_index()
                FI_SUM = px.line(MSK_SUM , x=X , y=Y , color=COLOR ,title= f'{Method} of {X} vs {Y} colored by {COLOR}')
                st.plotly_chart(FI_SUM , use_container_width=True,theme="streamlit") 
                
    with st.container():
        st.subheader("Custom EDA ('Distribution')")
        X_Dist_lst = ['Select' , 'order_item_quantity','order_profit_per_order','order_item_total','order_item_discount','order_item_profit_ratio','order_item_discount_rate',
                 'product_price','days_for_shipping_(real)','days_diff(schad_vs_real)']
        X_Dist = st.selectbox ('Select Line X :' , X_Dist_lst)
        if X_Dist == 'Select' :
            st.write(":red[Please Select x]")
        else:
            Dist_Fig = px.histogram(df ,x=X_Dist ,marginal='box' , title=f"Distribution of {X_Dist}")
            st.plotly_chart(Dist_Fig , use_container_width=True,theme="streamlit") 

