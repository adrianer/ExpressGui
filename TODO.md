1.Improve Gui
  Add menu to select server
  Add button to refresh
  make ui not ugly
2. Error handling
3. Add all commands of expressvpn
4. Create a function called parse_server_list.
  Takes an argument that is a string of the output of "expressvpn ls".
  Returns a list of servers. Each item being a dictionary that has the keys alias, country, location, recommended.

