import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.network.urlrequest import UrlRequest
from kivy.utils import get_color_from_hex
import json

kivy.require('2.1.0')

# Configuration - Change this to your backend IP
# For Android emulator: 10.0.2.2 usually
# For Genymotion: 10.0.3.2
# For local run: localhost or 127.0.0.1
API_URL = 'http://127.0.0.1:8000/scan/url'

class PhishingDetectorApp(App):
    def build(self):
        self.title = "PhishGuard Mobile"
        
        # Main Layout
        self.root = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # Header
        header = Label(
            text="PhishGuard Detector", 
            font_size='24sp', 
            size_hint=(1, 0.1),
            color=get_color_from_hex('#3498db')
        )
        self.root.add_widget(header)
        
        # Input Section
        self.url_input = TextInput(
            hint_text="Enter URL (e.g., http://example.com)",
            multiline=False,
            size_hint=(1, 0.1),
            padding_y=[15, 15]
        )
        self.root.add_widget(self.url_input)
        
        # Scan Button
        self.scan_btn = Button(
            text="Scan URL",
            size_hint=(1, 0.1),
            background_color=get_color_from_hex('#2ecc71')
        )
        self.scan_btn.bind(on_press=self.scan_url)
        self.root.add_widget(self.scan_btn)
        
        # Output Area
        self.output_scroll = ScrollView(size_hint=(1, 0.6))
        self.output_label = Label(
            text="Ready to scan...",
            size_hint_y=None,
            markup=True,
            halign='left',
            valign='top'
        )
        self.output_label.bind(texture_size=self.output_label.setter('size'))
        self.output_scroll.add_widget(self.output_label)
        self.root.add_widget(self.output_scroll)
        
        return self.root

    def scan_url(self, instance):
        url = self.url_input.text
        if not url:
            self.output_label.text = "[color=ff0000]Please enter a URL![/color]"
            return
            
        self.scan_btn.disabled = True
        self.output_label.text = "Scanning..."
        
        headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
        params = json.dumps({'url': url})
        
        # Make async request
        UrlRequest(
            API_URL, 
            req_body=params, 
            req_headers=headers,
            on_success=self.on_success,
            on_failure=self.on_failure,
            on_error=self.on_error,
            method='POST'
        )

    def on_success(self, req, result):
        self.scan_btn.disabled = False
        
        status = result.get('status', 'unknown')
        score = result.get('score', 0)
        details = result.get('details', [])
        
        color = "ff0000" if status == "phishing" else "00ff00"
        
        output_text = f"[b]Status:[/b] [color={color}]{status.upper()}[/color]\n"
        output_text += f"[b]Risk Score:[/b] {score}\n\n"
        output_text += "[b]Details:[/b]\n"
        
        if details:
            for detail in details:
                output_text += f"• {detail}\n"
        else:
            output_text += "No suspicious indicators found."
            
        self.output_label.text = output_text

    def on_failure(self, req, result):
        self.scan_btn.disabled = False
        self.output_label.text = f"[color=ff0000]Scan Failed. Server returned error.[/color]"

    def on_error(self, req, error):
        self.scan_btn.disabled = False
        self.output_label.text = f"[color=ff0000]Connection Error. Is backend running?\n{error}[/color]"

if __name__ == '__main__':
    PhishingDetectorApp().run()
