import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("WhatsApp Talk Trends")

uploaded_file = st.sidebar.file_uploader("Upload WhatsApp Chat Document")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)


    #fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove("group_notification")
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Demonstrate analysis regarding", user_list)

    if st.sidebar.button("Present Analysis"):

       # Stats Area
       num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)
       st.title("Top Statistics")

       # Define the layout with columns
       col1, col2, col3, col4 = st.columns(4)

       # Use consistent HTML with CSS for alignment
       with col1:
           st.markdown(
               """
               <div style='text-align: center;'>
                   <h3 style='margin: 0;'>Total Messages</h3>
                   <h2 style='margin: 0;'>{}</h2>
               </div>
               """.format(num_messages),
               unsafe_allow_html=True,
           )

       with col2:
           st.markdown(
               """
               <div style='text-align: center;'>
                   <h3 style='margin: 0;'>Total Words</h3>
                   <h2 style='margin: 0;'>{}</h2>
               </div>
               """.format(words),
               unsafe_allow_html=True,
           )

       with col3:
           st.markdown(
               """
               <div style='text-align: center;'>
                   <h3 style='margin: 0;'>Media Shared</h3>
                   <h2 style='margin: 0;'>{}</h2>
               </div>
               """.format(num_media_messages),
               unsafe_allow_html=True,
           )

       with col4:
           st.markdown(
               """
               <div style='text-align: center;'>
                   <h3 style='margin: 0;'>Links Shared</h3>
                   <h2 style='margin: 0;'>{}</h2>
               </div>
               """.format(num_links),
               unsafe_allow_html=True,
           )

       # monthly timeline
       st.title("Monthly Timeline")
       timeline = helper.monthly_timeline(selected_user, df)
       fig, ax = plt.subplots()
       ax.plot(timeline['time'], timeline['message'], color = 'green')
       plt.xticks(rotation = 'vertical')
       st.pyplot(fig)

       # daily timeline
       st.title("Daily Timeline")
       daily_timeline = helper.daily_timeline(selected_user, df)
       fig, ax = plt.subplots()
       ax.plot(daily_timeline['only_date'], daily_timeline['message'], color = 'green')
       plt.xticks(rotation = 'vertical')
       st.pyplot(fig)

       # activity map
       st.title("Activity Map")
       col1, col2 = st.columns(2)

       with col1:
           st.header("Most Busy Day")
           busy_day = helper.week_activity_map(selected_user, df)
           fig, ax = plt.subplots()
           ax.bar(busy_day.index, busy_day.values)
           plt.xticks(rotation='vertical')
           st.pyplot(fig)

       with col2:
           st.header("Most Busy Month")
           busy_month = helper.month_activity_map(selected_user, df)
           fig, ax = plt.subplots()
           ax.bar(busy_month.index, busy_month.values, color = 'orange')
           plt.xticks(rotation = 'vertical')
           st.pyplot(fig)


       st.title("Weekly Activity Map")
       user_heatmap = helper.activity_heat_map(selected_user, df)
       fig, ax = plt.subplots()
       ax = sns.heatmap(user_heatmap)
       st.pyplot(fig)






       # finding the busiest users in the group (Group Level)
       if selected_user == 'Overall':
           st.title("Most Active Members")
           x, new_df = helper.most_busy_users(df)
           fig, ax = plt.subplots()
           col1, col2 = st.columns(2)

           with col1:
                ax.bar(x.index, x.values, color = 'red')
                plt.xticks(rotation = 'vertical')
                st.pyplot(fig)

           with col2:
               st.dataframe(new_df)

       # WordCloud
       st.title("Text Visualization - WordCloud")
       df_wc = helper.create_wordcloud(selected_user, df)
       fig, ax = plt.subplots()
       ax.imshow(df_wc)
       st.pyplot(fig)

       # most common words
       st.title("Most Common Words")
       most_common_df = helper.most_common_words(selected_user, df)
       fig, ax = plt.subplots()
       ax.barh(most_common_df[0], most_common_df[1])
       plt.xticks(rotation = 'vertical')
       st.pyplot(fig)

       # emoji analysis
       # Emoji Analysis
       st.title("Emoji Analysis")

       emoji_df = helper.emoji_helper(selected_user, df)

       if emoji_df is None:
           st.markdown(f"####{selected_user} has not used any emojis while chatting 😊")
       else:
           col1, col2 = st.columns(2)

           with col1:
               st.dataframe(emoji_df)

           with col2:
               fig, ax = plt.subplots()
               ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f")
               st.pyplot(fig)







