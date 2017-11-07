kaToolsExpressionPicker

Thank you for visiting my tool!
This is module-based expression editor.
We can write vex/python code by drag & drop....plus a little bit of editing.
If you use one function over and over again, save it as a module, and you can grab it whenever you want from the list view!


**Installation

Put this repository somewhere and add its path to both:

-HOUDINI_PATH,
-HOUDINI_PYTHON_PANEL_PATH

in houdini.env.
(e.g. On Windows:
HOUDINI_PATH="C:/Users/foo/Documents/houdini16.0/kaToolsExpressionPicker;"
HOUDINI_PYTHON_PANEL_PATH="C:/Users/foo/Documents/houdini16.0/kaToolsExpressionPicker;")


Instructions
1. Type whatever code you might re-use.
2. Hit "Save".
3. Type Category and name, and press OK.
4. On the list, now you can see expressions you have saved.
5. Drag and Drop a parameter (e.g. "snippet" parameter in "attribwrangle")
6.Drag and drop expressions from the list onto text area.
7. You can edit code in the text area, Houdini shows result tight away.
    (Sorry, but no auto completion or syntax highlighting.)
    
    
Extra:
- When you have a bunch of expressions, you can filter expressions and categories.
- If you want to sort expressions, hit "sort".
- If you want to delete a expression you have in the list, select it and hit "delete".


**Shortcuts
(text area)
Ctrl + Shift + "+": zoom in
Ctrl + "-" : zoom out 


Bug....ish
- Drag and drop inside the list doesn't really work. It looks like you can re-arrange the order, but if you hit refresh, the list goes back to the previous order.
- If you press tab in the text area, cursor might jump to the end  of the text. 
- Even after you drag and drop a parameter, if you write something down on the parameter, it is not synced to the text area of this tool. (I wish the were completely synced each other.)



If you have any questions, feedbacks and/or ideas that may enhance usability of this tool, feel free to send a message to:
nkfxtd@gmail.com


Naoki K
