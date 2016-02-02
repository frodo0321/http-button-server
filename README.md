# http-button-server
An implementation of a Python HTTP Server for easy use of HTML buttons for inputs.
</br>
When a button is pressed, web page form state is sent to callback function as a query string.</br>


<h6>Usage:</h6>
1. Create a callback function:</br>
  def p(qs):</br>
  &emsp;print "BUTTON PRESSED", qs</br>
2. Create a ButtonServer object:</br>
	b=ButtonServer(p)</br>
3. Add buttons or textboxes to server:</br>
	b.add_button("Up", 'style="position: absolute; top: 0px; left: 0px;width: 60px;"')</br>
	b.add_button("Down", 'style="position: absolute; top: 20px; left: 0px; width: 60px;"')</br>
        b.add_textbox("tb", 'style="position: absolute; left: 200px; top: 0px"')</br>
        b.add_textbox("tb2", 'style="position: absolute; top: 0px; left: 60px"')</br>
4. Run server</br>
	b.run()</br>
