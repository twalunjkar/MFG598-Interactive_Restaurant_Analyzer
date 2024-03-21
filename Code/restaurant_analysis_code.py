# -*- coding: utf-8 -*-
"""
Created on Sun Apr 2 19:17:24 2023

@author: twalunjk

"""

import pandas as pd, tkinter as tk, folium, webbrowser, matplotlib.pyplot as plt
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

# Load the data from the Excel and CSV files
country_codes = pd.read_excel('country-code.xlsx')
zomato_data = pd.read_csv('zomato.csv', encoding='ISO-8859-1')

# Create a list of country names sorted alphabetically
country_names = sorted(country_codes['Country'].tolist())

class ZomatoApp:
    def __init__(self, master):                 #Initialize GUI for Restaurant Analysis Tool       
        # Set the style to 'clam'
        style = ttk.Style()
        style.theme_use('clam')

        # Change the background and foreground colors
        style.configure('TLabel', background='#FAEE73', foreground='#1E90FF')
        style.configure('TButton', background='#F0FFFF', foreground='#1E90FF')
        
        self.master = master
        master.title("Restaurant Analysis")
        
        # Set up the background image
        bg_image = Image.open("Media/cityscape.png")
        bg_image = bg_image.resize((master.winfo_screenwidth(), master.winfo_screenheight()), Image.ANTIALIAS)
        bg_image = ImageTk.PhotoImage(bg_image)
        bg_label = tk.Label(master, image=bg_image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        bg_label.image = bg_image  # keep a reference to prevent garbage collection
        
        # Add an introductory description
        intro_label = ttk.Label(master, text="\tWelcome to the Restaurant Analysis Tool!\n\nSelect a country and city to begin exploring restaurants in that area.", font=("Segoe Print", 14, "bold"), anchor="center")
        intro_label.pack(pady=20)
        
        # Create a label for the country selection
        country_label = ttk.Label(master, text="Select a country:",font=("Segoe Print", 12, "bold"))
        country_label.pack()
        
        # Create a combobox with the list of countries
        self.country_var = tk.StringVar()
        self.country_combobox = ttk.Combobox(master, textvariable=self.country_var, values=country_names)
        self.country_combobox.bind("<<ComboboxSelected>>", self.update_cities)
        self.country_combobox.pack()
        
        # Create a label for the city selection
        city_label = ttk.Label(master, text="Select a city:",font=("Segoe Print", 12, "bold"))
        city_label.pack()
        
        # Create a combobox for the cities, which will be populated based on the selected country
        self.city_var = tk.StringVar()
        self.city_combobox = ttk.Combobox(master, textvariable=self.city_var)
        self.city_combobox.pack()
        
        # Initialize the city combobox with the cities from the first country in the list
        self.update_cities()
        
        # Initialize a variable to hold the selected restaurants
        self.selected_restaurants = []
        
        # Create a button for the map view
        self.map_image = tk.PhotoImage(file="Media/mapView.png")
        map_button = ttk.Button(master, image=self.map_image, command=self.show_map)
        map_button.pack(side="left", padx=5.5, pady=10)
        
        # Create a button for the restaurant list view
        self.restaurant_list_image = tk.PhotoImage(file="Media/compareView.png")
        restaurant_list_button = ttk.Button(master, image=self.restaurant_list_image, command=self.update_restaurants)
        restaurant_list_button.pack(side="left", padx=5.5, pady=10)
                        
        # Create a button for the cuisine list view
        self.cuisine_list_image = tk.PhotoImage(file="Media/listView.png")
        cuisine_list_button = ttk.Button(master, image=self.cuisine_list_image, command=self.list_cuisines)
        cuisine_list_button.pack(side="left", padx=5.5, pady=10)
                        
        # Create a button to show the pie chart
        self.pie_chart_image = tk.PhotoImage(file="Media/chartView.png")
        pie_chart_button = ttk.Button(master, image=self.pie_chart_image, command=self.show_pie_chart)
        pie_chart_button.pack(side="left", padx=5.5, pady=10)
                        
        # Create a button to show the Review view
        self.review_filter_image = tk.PhotoImage(file="Media/reviewView.png")
        review_filter_button = ttk.Button(master, image=self.review_filter_image, command=self.review_filter)
        review_filter_button.pack(side="left", padx=5.5, pady=10)
               
        # Create a label for displaying the restaurant list
        self.restaurants_label = ttk.Label(master, text="")
        self.restaurants_label.pack()

    def update_cities(self, event=None):        #City List
    # Get the selected country code
        country_name = self.country_var.get()
        country_data = country_codes.loc[country_codes['Country'] == country_name]
        if len(country_data) > 0:
            country_code = country_data.iloc[0]['Country Code']
            
            # Filter the zomato data to only include restaurants in the selected country
            country_data = zomato_data[zomato_data['Country Code'] == country_code]
            
            # Get the unique cities in the filtered data and sort them alphabetically
            cities = sorted(country_data['City'].unique().tolist())
            
            # Update the city combobox with the list of cities for the selected country
            self.city_combobox.config(values=cities)

    def show_map(self):                         #Map View
        
        if not self.country_var.get() or not self.city_var.get():
            messagebox.showerror("Error", "Please select a country and a city.")
        else:
            # Show the map
            pass
        
            # Get the selected city name
            city_name = self.city_var.get()
            
            # Filter the zomato data to only include restaurants in the selected city
            city_data = zomato_data[zomato_data['City'] == city_name]
            
            # Create a map centered on the first restaurant in the city
            if len(city_data) > 0:
                lat = city_data.iloc[0]['Latitude']
                lon = city_data.iloc[0]['Longitude']
                map = folium.Map(location=[lat, lon], zoom_start=12)
                
                # Add markers for each restaurant in the city
                for i, row in city_data.iterrows():
                    lat = row['Latitude']
                    lon = row['Longitude']
                    name = row['Restaurant Name']
                    cost = row['Average Cost for two']
                    currency = row['Currency']
                    rating = row['Aggregate rating']
                    locality = row['Locality']
                    
                    # Create a popup with the restaurant information
                    #popup = f'<strong>{name}</strong><br>Average cost for two: {cost} {currency}<br>Rating: {rating}/5<br>Locality: {locality}'
                    popup = f'<span style="color:#1E90FF;font-family:Segoe Print;font-size:10pt"><strong>{name}<strong></span><br><span style="color:#000000;font-family:Segoe Print;font-size:8pt">Average cost for two: </span><span style="color:#1E90FF;font-family:Segoe Print;font-size:10pt">{cost} {currency}</span><br><span style="color:#000000;font-family:Segoe Print;font-size:8pt">Rating: </span><span style="color:#1E90FF;font-family:Segoe Print;font-size:10pt">{rating}/5</span><br><span style="color:#000000;font-family:Segoe Print;font-size:8pt">Locality: </span><span style="color:#1E90FF;font-family:Segoe Print;font-size:10pt">{locality}</span>'

                    # Add the marker to the map
                    #folium.Marker([lat, lon], popup=popup).add_to(map)
                    folium.Marker([lat, lon], popup=popup, icon=folium.Icon(icon='cutlery')).add_to(map)
                    
                # Display the map in a new window
                map.save('map.html')
                webbrowser.open('map.html')

    def update_restaurants(self, event=None):   #Compare View
        if not self.country_var.get() or not self.city_var.get():
            messagebox.showerror("Error", "Please select a country and a city.")
        else:
            # Update the restaurant list
            pass
        
            # Get the selected city
            city_name = self.city_var.get()
        
            # Filter the zomato data to only include restaurants in the selected city
            city_data = zomato_data[zomato_data['City'] == city_name]
        
            # Get the unique restaurant names in the filtered data and sort them alphabetically
            restaurants = sorted(city_data['Restaurant Name'].unique().tolist())
        
            def select_restaurants():               
                if not self.restaurant1_var.get() or not self.restaurant2_var.get():
                    messagebox.showerror("Error", "Please select 2 restaurants to compare.")
                else:
                    # Update the restaurant list
                    pass                    
                    
                    # Get the selected restaurants
                    restaurant1 = self.restaurant1_var.get()
                    restaurant2 = self.restaurant2_var.get()
                
                    # Filter the zomato data to only include the selected restaurants
                    selected_restaurants = city_data[(city_data['Restaurant Name'] == restaurant1) | (city_data['Restaurant Name'] == restaurant2)]
                
                    # Get the price range, rating and vote count for each selected restaurant and display it in a tabular form
                    restaurant_data = selected_restaurants[['Restaurant Name', 'Price range', 'Rating text', 'Votes','Has Table booking','Has Online delivery','Is delivering now']]
                    restaurant_data = restaurant_data.set_index('Restaurant Name')
                    restaurant_data = restaurant_data.transpose()  # transpose the DataFrame
                    restaurant_table = ttk.Treeview(self.compare_window)
                    restaurant_table['columns'] = restaurant_data.columns.tolist()  # set the columns to the index values of the transposed DataFrame
                    restaurant_table.column('#0', width=200, anchor=tk.W)
                    for col in restaurant_data.columns:
                        restaurant_table.column(col, width=100, anchor=tk.CENTER)
                        restaurant_table.heading(col, text=col)
                    for index, row in restaurant_data.iterrows():
                        restaurant_table.insert('', 'end', text=index, values=tuple(row))
                        
                    # Add the label for the restaurant selection to the tabular form
                    # restaurant_label = ttk.Label(self.compare_window, text="Selected Restaurants:")
                    # restaurant_label.pack()
                    restaurant_label = ttk.Label(self.compare_window, text="Selected Restaurants:", background="#F0FFFF", foreground="#1E90FF")
                    restaurant_label.pack()

                    # Display the tabular form and the label for the restaurant selection
                    restaurant_table.pack()
                                    
            # Create a new window for displaying the selected restaurants
            self.compare_window = tk.Toplevel(self.master)
            self.compare_window.title('Compare Restaurants')
            self.compare_window.geometry('500x400')
            
            # Set the background color of the window
            self.compare_window.configure(background='#F0FFFF')
            
            # Create a combobox for the first selected restaurant
            self.restaurant1_var = tk.StringVar()
            self.restaurant1_combobox = ttk.Combobox(self.compare_window, textvariable=self.restaurant1_var, values=restaurants)
            self.restaurant1_combobox.pack()
            
            # Create a combobox for the second selected restaurant
            self.restaurant2_var = tk.StringVar()
            self.restaurant2_combobox = ttk.Combobox(self.compare_window, textvariable=self.restaurant2_var, values=restaurants)
            self.restaurant2_combobox.pack()
            
            def restaurant1_selected(event):
                # Get the selected restaurant in the first combobox
                selected_restaurant = self.restaurant1_var.get()
            
                # Update the values of the second combobox to exclude the selected restaurant
                remaining_restaurants = [r for r in restaurants if r != selected_restaurant]
                self.restaurant2_combobox['values'] = remaining_restaurants
            
            # Bind the event when a restaurant is selected in the first combobox
            self.restaurant1_combobox.bind('<<ComboboxSelected>>', restaurant1_selected)
            
            # Create a button to submit the selected restaurants and display their price range        
            select_button = ttk.Button(self.compare_window, text="Compare", command=select_restaurants)
            select_button.pack()
                        
    def list_cuisines(self):                    #Cuisine List
        # Get the unique cuisines and sort them alphabetically
        cuisines = zomato_data['Cuisines'].str.split(',').explode().str.strip().unique().tolist()
        cuisines = sorted([str(cuisine) for cuisine in cuisines if cuisine])
        
        # Create a dialog box with a combobox to select a cuisine
        cuisine_selection = tk.Toplevel(self.master)
        # Change the background color of the window
        cuisine_selection.configure(background="#F0FFFF")
        cuisine_selection.title("Select Cuisine")
        cuisine_selection.geometry("200x150")
        cuisine_selection.resizable(False, False)
    
        # Add a label for the combobox
        cuisine_label = tk.Label(cuisine_selection, text="Select a cuisine:")
        # Change the foreground color of the label
        cuisine_label.configure(foreground="#1E90FF")
        cuisine_label.pack(padx=10, pady=10)
                
        # Create a combobox to select a cuisine
        selected_cuisine = tk.StringVar()
        selected_cuisine.set(cuisines[0])
        cuisine_combobox = ttk.Combobox(cuisine_selection, textvariable=selected_cuisine, values=cuisines, state="readonly")
        cuisine_combobox.pack(padx=10, pady=10)
    
        def get_restaurants():
            # Get the selected cuisine from the combobox
            selected_cuisine_value = selected_cuisine.get()
        
            if not selected_cuisine_value:
                # Display an error message if no cuisine is selected
                tk.messagebox.showerror("Error", "Please select a cuisine")
            else:
                # Filter the zomato_data dataframe for restaurants that serve the selected cuisine
                mask = zomato_data['Cuisines'].notna() & zomato_data['Cuisines'].str.contains(selected_cuisine_value)
                selected_restaurants = zomato_data.loc[mask, ['Restaurant Name', 'City','Country Code']]
        
                # Add a column for country names based on country codes
                country_codes = pd.read_excel('Country-Code.xlsx')
                country_dict = dict(zip(country_codes['Country Code'], country_codes['Country']))
                selected_restaurants['Country'] = selected_restaurants['Country Code'].map(country_dict)
        
                # Create a dialog box to display the list of restaurants with details
                restaurant_selection = tk.Toplevel(self.master)
                restaurant_selection.configure(background="#F0FFFF")
                restaurant_selection.title(f"{selected_cuisine_value} restaurants")
                restaurant_selection.geometry("600x400")
                restaurant_selection.resizable(False, False)
                
                # Create a frame to hold the table and scrollbar
                frame = ttk.Frame(restaurant_selection)
                frame.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH, expand=True)
        
                # Create a table to display the list of restaurants with headings
                headings = ['Restaurant Name', 'City','Country Code', 'Country']
                column_widths = [200, 100, 100, 100]
                tree = ttk.Treeview(restaurant_selection, columns=headings, show="headings")
                for column, width in zip(headings, column_widths):
                    tree.column(column, width=width)
                    tree.heading(column, text=column)
                    
                # Add the table to the frame and configure the scrollbar
                vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
                vsb.pack(side=tk.RIGHT, fill=tk.Y)
                tree.configure(yscrollcommand=vsb.set)
                tree.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)
                
                def on_select(event):
                    # Get the selected row
                    selected_row = tree.selection()[0]
                    
                    # Get the restaurant name from the selected row
                    restaurant_name = tree.item(selected_row, 'values')[0]
                    
                    # Get the price range, rating and vote count for the selected restaurant
                    mask = zomato_data['Restaurant Name'] == restaurant_name
                    selected_restaurant = zomato_data.loc[mask, ['Restaurant ID', 'Address', 'Locality Verbose', 'Cuisines', 'Average Cost for two', 'Currency', 'Has Table booking', 'Has Online delivery', 'Is delivering now', 'Aggregate rating', 'Rating text', 'Votes']]
                    
                    # Display the details in a message box
                    details = f"Restaurant ID: {selected_restaurant.iloc[0]['Restaurant ID']}\nAddress: {selected_restaurant.iloc[0]['Address']}\nLocality Verbose: {selected_restaurant.iloc[0]['Locality Verbose']}\nCuisines: {selected_restaurant.iloc[0]['Cuisines']}\nAverage Cost for two: {selected_restaurant.iloc[0]['Average Cost for two']} {selected_restaurant.iloc[0]['Currency']}\nHas Table booking: {selected_restaurant.iloc[0]['Has Table booking']}\nHas Online delivery: {selected_restaurant.iloc[0]['Has Online delivery']}\nIs delivering now: {selected_restaurant.iloc[0]['Is delivering now']}\nAggregate rating: {selected_restaurant.iloc[0]['Aggregate rating']}\nRating text: {selected_restaurant.iloc[0]['Rating text']}\nVotes: {selected_restaurant.iloc[0]['Votes']}"
                    
                    tk.messagebox.showinfo(restaurant_name, details)
                    
                # Bind the on_select function to the selection event of the table
                tree.bind("<Double-1>", on_select)
        
                # Add the list of restaurants with details to the table
                for index, row in selected_restaurants.iterrows():
                    tree.insert("", tk.END, values=list(row))
        
        select_button = tk.Button(cuisine_selection, text="Show Restaurants", command=get_restaurants)
        select_button.configure(background="#F0FFFF", foreground="#1E90FF")
        # Change the foreground color of the label
        cuisine_label.configure(foreground="#1E90FF")
        select_button.pack(pady=10)
        
    def show_pie_chart(self):                   #Rating Distribution
        
        if not self.country_var.get() or not self.city_var.get():
            messagebox.showerror("Error", "Please select a country and a city.")
        else:
            # Show the map
            pass
        
            # Get the selected city
            city_name = self.city_var.get()
            
            # Filter the zomato data to only include restaurants in the selected city
            city_data = zomato_data[zomato_data['City'] == city_name]
        
            # Calculate the count of restaurants for each aggregate rating and rating color
            agg_rating_counts = city_data['Aggregate rating'].value_counts()
            rating_color_counts = city_data['Rating color'].value_counts()
            
            # Extract the labels and counts for the inner pie chart
            agg_rating_labels = agg_rating_counts.index.tolist()
            agg_rating_values = agg_rating_counts.values.tolist()
            
            # Extract the labels and counts for the outer pie chart
            rating_color_labels = rating_color_counts.index.tolist()
            rating_color_values = rating_color_counts.values.tolist()
        
            # Plot the nested pie chart
            fig, ax = plt.subplots(figsize=(8, 8))
        
            # Outer pie chart
            # Define a dictionary to map rating color labels to colors
            color_map = {
                'Dark Green': '#006400',
                'Green': '#008000',
                'Yellow': '#FFFF00',
                'Orange': '#FFA500',
                'Red': '#FF0000',
                'Dark Red': '#8B0000'
            }
            
            # Map the rating color labels to colors using the dictionary
            outer_colors = [color_map[color] for color in rating_color_labels]
            #outer_colors = rating_color_labels
            outer_values = rating_color_values
            outer_labels = rating_color_labels
        
            # Inner pie chart
            inner_colors = ['brown', 'indigo', 'b', 'y', 'c', 'm', 'k', 'gray','teal']
            inner_values = []
            inner_labels = []
        
            for i, color in enumerate(rating_color_labels):
                agg_ratings = city_data[city_data['Rating color'] == color]['Aggregate rating']
                agg_ratings_counts = agg_ratings.value_counts()
                agg_ratings_labels = agg_ratings_counts.index.tolist()
                agg_ratings_values = agg_ratings_counts.values.tolist()
        
                for j, agg_rating in enumerate(agg_ratings_labels):
                    inner_values.append(agg_ratings_values[j])
                    inner_labels.append(str(agg_rating) + ' (' + str(agg_ratings_values[j]) + ')')
        
            inner_colors = [inner_colors[i % len(inner_colors)] for i in range(len(inner_labels))]
        
            #ax.pie(outer_values, labels=outer_labels, colors=outer_colors,
                   #radius=1, wedgeprops=dict(width=0.3, edgecolor='w'))
            # Use the mapped colors as the outer_colors list
            ax.pie(outer_values, labels=outer_labels, colors=outer_colors,
                   radius=1, wedgeprops=dict(width=0.3, edgecolor='w'))
        
            ax.pie(inner_values, labels=inner_labels, colors=inner_colors,
                   radius=1-0.3, wedgeprops=dict(width=0.4, edgecolor='w'))
        
            ax.set(aspect="equal")
            plt.title('Aggregate Rating (inner) vs Rating Color (outer) for ' + city_name)
            plt.savefig('Media/pieCharts.png')
            plt.show()
            # Open the image file
            img = Image.open('Media/pieCharts.png')
            # Show the image
            img.show()

    def review_filter(self):                    #Review Filter
        
        if not self.country_var.get() or not self.city_var.get():
            messagebox.showerror("Error", "Please select a country and a city.")
        else:
            # Show the map
            pass
            # Get the selected city name
            city_name = self.city_var.get()
            
            # Filter the zomato data to only include restaurants in the selected city
            city_data = zomato_data[zomato_data['City'] == city_name]
            
            # Create a new window to display the filtered data
            filter_window = tk.Toplevel(self.master)
            filter_window.title("Filtered Restaurants")
            
            # Create a frame to hold the table and scrollbar
            table_frame = ttk.Frame(filter_window)
            table_frame.pack(padx=10, pady=10, fill='both', expand=True)
            
            # Create a table to display the filtered data
            table = ttk.Treeview(table_frame, columns=('name', 'locality', 'rating'), show='headings')
            table.heading('name', text='Restaurant Name')
            table.heading('locality', text='Locality')
            table.heading('rating', text='Aggregate Rating')
            table.pack(side='left', fill='both', expand=True)
            
            # Create a scrollbar for the table
            scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=table.yview)
            scrollbar.pack(side='right', fill='y')
            
            # Configure the table to use the scrollbar
            table.configure(yscrollcommand=scrollbar.set)
            
            # Populate the table with the filtered data
            for i, row in city_data.iterrows():
                table.insert('', 'end', values=(row['Restaurant Name'], row['Locality'], row['Aggregate rating']))
                
            # Create a filter frame to allow the user to filter the data by rating
            filter_frame = ttk.Frame(filter_window)
            filter_frame.pack(pady=10)
            
            # Create a label for the filter options
            filter_label = ttk.Label(filter_frame, text="Filter by Aggregate Rating:")
            filter_label.pack(side='left')
            
            # Create a combobox with the filter options
            filter_var = tk.StringVar()
            filter_combobox = ttk.Combobox(filter_frame, textvariable=filter_var, values=['Less than 3', 'More than 3', 'More than 4', 'More than 4.5'])
            filter_combobox.pack(side='left')
            
            # Create a filter function to update the table based on the selected filter
            def update_table(event=None):
                # Get the selected filter value
                filter_value = filter_var.get()
                
                # Filter the data based on the selected filter
                if filter_value == 'Less than 3':
                    filtered_data = city_data[city_data['Aggregate rating'] < 3.0]
                elif filter_value == 'More than 3':
                    filtered_data = city_data[city_data['Aggregate rating'] > 3.0]
                elif filter_value == 'More than 4':
                    filtered_data = city_data[city_data['Aggregate rating'] > 4.0]
                elif filter_value == 'More than 4.5':
                    filtered_data = city_data[city_data['Aggregate rating'] > 4.5]
                else:
                    filtered_data = city_data
                
                # Clear the table and repopulate it with the filtered data
                table.delete(*table.get_children())
                for i, row in filtered_data.iterrows():
                    table.insert('', 'end', values=(row['Restaurant Name'], row['Locality'], row['Aggregate rating']))
            
            # Bind the filter function to the combobox selection event
            filter_combobox.bind("<<ComboboxSelected>>", update_table)
            
            # Call the filter function to populate the table with the initial data
            update_table()
    
# Create the main window and start the GUI event loop
root = tk.Tk()
root.geometry("900x700+0+0")
root.state("zoomed")
app = ZomatoApp(root)
# set the window background color to red
root.configure(bg='#F0FFFF')
root.mainloop()