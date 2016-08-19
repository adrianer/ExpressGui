1. Error handling
2. Add Preferences in gui
3. Move parsing functions to own file
4. Add support for menubar?
5. Make widgets seperate classes?
6. Use GObject signals?
7. Get default server selection
8. Locaiton dialog needs to be dialog class?

Bugs
It shouldn't try to connect when already connected and open for the first time.
When opened and not connected and the choose location button is pressed. The location combobox is blank.
Connect gets called twice? might be an issues with the way the toggle switch works.
Choose location dialog can be opened a billion times.