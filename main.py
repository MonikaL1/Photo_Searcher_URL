from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder

import wikipedia
import requests

Builder.load_file('frontend.kv')

class FirstScreen(Screen):
    def search_image(self):
        try:
            # Get user query from TextInput
            query = self.manager.current_screen.ids.user_query.text
            # Get wikipedia page and the first image link
            page = wikipedia.page(query)
            image_link = page.images[0]

            # Add User-Agent header to the request
            headers = {'User-Agent': 'Mozilla/5.0'}
            req = requests.get(image_link, headers=headers)
            if req.status_code == 200:
                # Download the image
                imagepath = 'files/image.jpg'
                with open(imagepath, "wb") as file:
                    file.write(req.content)
                # Set the image in the Image widget
                self.manager.current_screen.ids.img.source = imagepath
                print("Image downloaded successfully")
            else:
                print("Failed to download image:", req.status_code)
        except wikipedia.exceptions.DisambiguationError as e:
            print("Wikipedia disambiguation error:", e.options)
        except wikipedia.exceptions.PageError:
            print("Wikipedia page not found for query:", query)
        except requests.RequestException as e:
            print("Error downloading image:", e)

class RootWidget(ScreenManager):
    pass

class MainApp(App):
    def build(self):
        return RootWidget()

MainApp().run()
