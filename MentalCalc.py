"""
Copyright 2026 Martin Groß <martin@cavedev.de>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the “Software”), to deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit
persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of
the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

# Import statements for wxPython and the mental_calc module that contains the code to generate the exercise sheet
# as a Word document.
import wx
import mental_calc as mc
import datetime

# Define the MentalCalcFrame class that represents the main GUI frame for the MentalCalc application.
class MentalCalcFrame(wx.Frame):
    """
    A GUI frame for the MentalCalc application.
    """

    def __init__(self, *args, **kwargs):
        # Initialize the parent class.
        super(MentalCalcFrame, self).__init__(*args, **kwargs)

        # field for exercise controls
        self.exercise_controls = None

        # create the main panel
        self.create_main_gui()

        # create a menu bar
        self.make_menu_bar()

        # and a status bar
        self.CreateStatusBar()
        self.SetStatusText("Welcome to Mental Calc!")

    def create_main_gui(self):
        # Create a panel to hold all other widgets.
        panel = wx.Panel(self)

        # Create a grid of 6 rows (including a spacer row) and 3 columns:
        # 6 rows total: 1 header row + 1 spacer row + 4 data rows; 3 columns
        grid = wx.FlexGridSizer(rows=6, cols=3, vgap=4, hgap=10)

        # Make the last two columns grow so text fields expand with the window
        grid.AddGrowableCol(1)  # 2nd column
        grid.AddGrowableCol(2)  # 3rd column

        # Header row (labels only)
        hdr1 = wx.StaticText(panel, label="Exercise type")
        hdr2 = wx.StaticText(panel, label="Min. value")
        hdr3 = wx.StaticText(panel, label="Max. value")

        # (Optional) make headers bold
        # for hdr in (hdr1, hdr2, hdr3):
        #     font = hdr.GetFont()
            # font.MakeBold()
            # font.PointSize += 1
            # hdr.SetFont(font)

        # Add the headers to the grid
        grid.Add(hdr1, flag=wx.ALIGN_CENTER_VERTICAL)
        grid.Add(hdr2, flag=wx.ALIGN_CENTER_VERTICAL)
        grid.Add(hdr3, flag=wx.ALIGN_CENTER_VERTICAL)

        # Add a little space between the header row and the data rows
        for _ in range(3):
            grid.AddSpacer(2)

        # Exercise types as a list of enum values
        exercise_types = [mc.ExerciseType.ADD,
                     mc.ExerciseType.SUB,
                     mc.ExerciseType.MUL,
                     mc.ExerciseType.DIV]

        # Keep references to all controls by exercise name
        self.exercise_controls = {}

        # Create and add controls for each exercise row
        for exercise_type in exercise_types:
            chk = wx.CheckBox(panel, label=exercise_type.value)
            chk.Bind(wx.EVT_CHECKBOX, self.text_control_toggle)

            # Text fields for min and max values
            min_ctrl = wx.TextCtrl(panel, value=str(mc.DEFAULT_LIMITS_FOR_TYPE[exercise_type][0]))
            min_ctrl.SetHint("Value >= 0")
            max_ctrl = wx.TextCtrl(panel, value=str(mc.DEFAULT_LIMITS_FOR_TYPE[exercise_type][1]))
            max_ctrl.SetHint("Value <= 100")

            # Initially disable the text controls
            min_ctrl.Disable()
            max_ctrl.Disable()

            # Store references for later access
            self.exercise_controls[exercise_type.value] = {
                "check": chk,
                "min": min_ctrl,
                "max": max_ctrl,
            }

            # add the checkbox and text fields to the grid
            grid.Add(chk, flag=wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL)
            grid.Add(min_ctrl, flag=wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND)
            grid.Add(max_ctrl, flag=wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND)

        # Wrap grid in a BoxSizer for a nice border
        outer = wx.BoxSizer(wx.VERTICAL)
        outer.Add(grid, proportion=1, flag=wx.ALL | wx.EXPAND, border=12)

        # Add a button to generate the exercise_types below the grid
        generate_exercises_button = wx.Button(panel, label="Generate exercises")
        generate_exercises_button.Bind(wx.EVT_BUTTON, self.generate_exercises)
        outer.Add(generate_exercises_button, flag=wx.ALL | wx.ALIGN_RIGHT, border=12)
        panel.SetSizer(outer)


    def make_menu_bar(self):
        """
        A menu bar is composed of menus, which are composed of menu items.
        This method builds a set of menus and binds handlers to be called
        when the menu item is selected.
        """

        # Make a file menu with Hello and Exit items
        file_menu = wx.Menu()
        # # The "\t..." syntax defines an accelerator key that also triggers
        # # the same event
        # helloItem = file_menu.Append(-1, "&Hello...\tCtrl-H",
        #                             "Help string shown in status bar for this menu item")
        file_menu.AppendSeparator()
        # When using a stock ID, we don't need to specify the menu item's
        # label
        exit_item = file_menu.Append(wx.ID_EXIT)

        # Now a help menu for the about item
        help_menu = wx.Menu()
        about_item = help_menu.Append(wx.ID_ABOUT)

        # Make the menu bar and add the two menus to it. The '&' defines
        # that the next letter is the "mnemonic" for the menu item. On the
        # platforms that support it, those letters are underlined and can be
        # triggered from the keyboard.
        menu_bar = wx.MenuBar()
        menu_bar.Append(file_menu, "&File")
        menu_bar.Append(help_menu, "&Help")

        # Give the menu bar to the frame
        self.SetMenuBar(menu_bar)

        # Finally, associate a handler function with the EVT_MENU event for
        # each of the menu items. That means that when that menu item is
        #  activated, then the associated handler function will be called.
        # self.Bind(wx.EVT_MENU, self.OnHello, helloItem)
        self.Bind(wx.EVT_MENU, self.on_exit, exit_item)
        self.Bind(wx.EVT_MENU, self.on_about, about_item)


    def on_exit(self, event):
        """Close the frame, terminating the application."""
        self.Close(True)

    # def OnHello(self, event):
    #     """Say hello to the user."""
    #     wx.MessageBox("Hello again from wxPython")


    def on_about(self, event):
        """Display an About Dialog"""
        wx.MessageBox("This is a GUI for Mental Calc,"
                      " a simple script to generate exercise sheets for mental arithmetic.\n"
                      "Written by Martin Groß in order to torment innocent children ;-)",
                      "About Mental Calc",
                      wx.OK | wx.ICON_INFORMATION)


    def text_control_toggle(self, event):
        enable = event.IsChecked()

        # get the exercise name from the checkbox label
        exercise_name = event.EventObject.GetLabel()

        # toggle the appropriate text controls
        for control_name in ("min", "max"):
            self.exercise_controls[exercise_name][control_name].Enable(enable)


    def get_limits_for_type(self) -> dict[mc.ExerciseType, tuple[int, int]]:
        limits = {}

        # Read the limits from the user input (check boxes and text fields)
        for exercise_type in mc.ExerciseType:
            # Status of the checkbox
            if self.exercise_controls[exercise_type.value]["check"].IsChecked():
                # Get the minimum limit
                min_limit = self.exercise_controls[exercise_type.value]["min"].GetValue()

                # Check if the min limit is valid
                if min_limit.isdigit() and int(min_limit) >= 0:
                    min_limit = int(min_limit)
                else:
                    min_limit = mc.DEFAULT_LIMITS_FOR_TYPE[exercise_type][0]
                    self.SetStatusText(f"Invalid min limit for {exercise_type.value}, using default: {min_limit}")
                    self.exercise_controls[exercise_type.value]["min"].SetValue(str(min_limit))

                # Get the maximum limit
                max_limit = self.exercise_controls[exercise_type.value]["max"].GetValue()

                # Check if the max limit is valid
                if max_limit.isdigit() and int(max_limit) <= 100:
                    max_limit = int(max_limit)
                else:
                    max_limit = mc.DEFAULT_LIMITS_FOR_TYPE[exercise_type][1]
                    self.SetStatusText(f"Invalid max limit for {exercise_type.value}, using default: {max_limit}")
                    self.exercise_controls[exercise_type.value]["max"].SetValue(str(max_limit))

                # Store the limits for the exercise type
                limits[exercise_type] = (min_limit, max_limit)

        return limits


    def generate_exercises(self, event):
        # Check if any exercise type is selected
        limits_for_type = self.get_limits_for_type()
        if not limits_for_type:
            # Show error message
            wx.MessageBox("Please select at least one exercise type and specify valid limits!",
                          "Error",
                          wx.OK | wx.ICON_ERROR)
            return

        # generate a default file name
        filename_with_timestamp = \
            datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '_mental_calc.docx'

        # Open a file dialog and ask the user for a filename
        dlg = wx.FileDialog(self, "Save file as ...",
                            defaultDir=wx.StandardPaths.Get().GetUserDataDir(),
                            defaultFile=filename_with_timestamp,
                            style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetPath()
            number_of_pages = 2
            number_of_columns = 3
            exercises = mc.generate_exercises(
                51 * number_of_pages,
                limits_for_type)
            mc.generate_word_document(exercises, number_of_columns, filename)
            self.SetStatusText("Saved as: " + filename)
        else:
            return

# C
if __name__ == '__main__':
    # When this module is run (not imported), then create the app, the
    # frame, show it, and start the event loop.
    app = wx.App()
    frm = MentalCalcFrame(None, title='Mental Calc', size=(400, 280))
    frm.Show()
    app.MainLoop()