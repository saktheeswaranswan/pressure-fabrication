# -*- coding: utf-8 -*-
"""
MIT License

Copyright (c) 2020 tamalone1
"""
import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from .PressureVessels import Vessel

# Set plt dpi
plt.rcParams['figure.dpi'] = 280

# GUI class to create and manage the GUI
class PV_GUI(tk.Frame):
    # Create a GUI to interactively calculate pressure vessel stresses
    inputfields = ('External pressure',
                   'Internal pressure',
                   'Outer diameter',
                   'Inner diameter',
                   'Yield stress',
                   'Derated Yield (400F)')

    outputfields = ('Average Linear Stress',
                    'Maximum Local Stress',
                    'Internal Pressure for Burst',
                    'External Pressure for Collapse',
                    'Minimum Safety Factor')
    defaultvalues = (15, 0, 1.695, 1.460, 120, 116)

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.configure(background='azure')

        # Create a vessel instance for the calculations
        self.vessel = Vessel(*self.defaultvalues)

        # Create the input entry fields
        inputframe = tk.Frame(self, background=self['background'])
        self.ent = self.buildinputtable(inputframe)
        inputframe.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        # Add radio buttons for units
        frame2 = tk.Frame(self, background=self['background'])
        ''' Not yet implemented
        units = tk.StringVar()
        units.set('0')
        radioUS = tk.Radiobutton(frame2, text='US Customary',
                                 value='US Customary', variable=units,
                                 width=15, background=self['background'])
                                # , command=lambda e=self.ent:unitselect(e))
        radioUS.grid(row=0, column=0, sticky='e')
        radioMetric = tk.Radiobutton(frame2, text='Metric', value='Metric',
                                     variable=units, width=15,
                                     background=self['background'])
                                    #, command=lambda e=self.ent:unitselect(e))
        radioMetric.grid(row = 0, column = 1, sticky = 'w')
        '''
        frame2.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

        # Create the output table
        outputframe = tk.Frame(self, background=self['background'])
        self.outputs = self.buildoutputtable(outputframe)
        outputframe.grid(row=2, column=0, columnspan=2, padx=10, pady=10,
                         sticky='nsew')

        # Insert calculate button
        buttonrowframe = tk.Frame(self, background=self['background'])
        button1 = tk.Button(buttonrowframe, text='Calculate', width=20,
                            command=self.update_results)
        button1.pack(side=tk.TOP)
        buttonrowframe.grid(row=1, column=0, columnspan=2, padx=10, pady=10,
                            sticky='nsew')

        # Set the focus to the first entry box
        self.ent['External pressure'].focus_set()

    def entryhighlight(self, event):
        # Change entry color to indicate hovering over it
        event.widget['background'] = 'honeydew'
        event.widget['foreground'] = '#000000'

    def entryrevert(self, event):
        # Change entry color after moving off of entry
        event.widget['background'] = 'white'
        event.widget['foreground'] = '#05322B'

    def buildinputtable(self, root):
        # Display entry boxes for each inputfield
        # Return dictionary of inputfield:entry pairs
        entries = {}
        for i, field in enumerate(self.inputfields):
            lab = tk.Label(root, width=20, text=field + ': ', anchor='e',
                           font=('Arial 12'), background=self['background'])
            lab.grid(row=i, column=0, padx=2, pady=2)
            ent = tk.Entry(root, width=20, font=('Arial 12'),
                           justify=tk.CENTER, foreground='#05322B')
            ent.insert(0, self.defaultvalues[i])
            ent.bind('<Enter>', self.entryhighlight)
            ent.bind('<Leave>', self.entryrevert)
            ent.grid(row=i, column=1, padx=2, pady=2)

            entries[field] = ent

        return entries

    def buildoutputtable(self, root):
        # Build the output table and store the label objects used to display
        # the values
        # outputrow1 = len(inputfields) + 2

        # Assemble output table header
        lab = tk.Label(root, width=20, text='Calculated Stress:', anchor='c',
                       font=('Arial 12'), background=self['background'])
        lab.grid(row=1, column=1, padx=2, pady=2)
        lab = tk.Label(root, width=20, text='Allowable Stress:', anchor='c',
                       font=('Arial 12'), background=self['background'])
        lab.grid(row=0, column=2, columnspan=2, padx=2, pady=2)
        lab = tk.Label(root, width=20, text='(room temperature)', anchor='c',
                       font=('Arial 12'), background=self['background'])
        lab.grid(row=1, column=2, padx=2, pady=2)
        lab = tk.Label(root, width=20, text='(derated temperature)',
                       anchor='c', font=('Arial 12'),
                       background=self['background'])
        lab.grid(row=1, column=3, padx=2, pady=2)

        # Assemble output table
        outputs = {}
        for i, field in enumerate(self.outputfields):
            # Store the created labels in a dictionary for later
            outputs[field] = {}
            # Skip the first two rows (already built)
            currentrow = i + 2
            # First label is the actual field name
            lab = tk.Label(root, text=field+': ', anchor='e',
                           font=('Arial 12'), background=self['background'])
            # These fields will show additional values in the first column
            if field in ('Average Linear Stress', 'Maximum Local Stress'):
                # if data in column 1, place label as normal in column 0
                lab.grid(row=currentrow, column=0, padx=2, pady=2)
                lab = tk.Label(root, width=20, text='0', anchor='c',
                               relief=tk.GROOVE, font=('Arial 12'),
                               background=self['background'])
                lab.grid(row=currentrow, column=1, padx=2, pady=2)
                # For each field, store the label in a corresponding subfield
                outputs[field]['calculated'] = lab
            else:
                # If no data in column 1, make the label span columns 0 and 1
                lab.grid(row=currentrow, column=0, padx=2, pady=2,
                         columnspan=2)

            # All fields will show values in columns 2 and 3
            lab = tk.Label(root, width=20, text='0', anchor='c',
                           relief=tk.GROOVE, font=('Arial 12'),
                           background=self['background'])
            lab.grid(row=currentrow, column=2, padx=2, pady=2)
            # For each field, store the label in a corresponding subfield
            outputs[field]['room'] = lab
            lab = tk.Label(root, width=20, text='0', anchor='c',
                           relief=tk.GROOVE, font=('Arial 12'),
                           background=self['background'])
            lab.grid(row=currentrow, column=3, padx=2, pady=2)
            outputs[field]['derated'] = lab

        # for each key in the outputs dictionary, the value is a
        # sub-dictionary containing the label objects for each column
        return outputs

    def get_entryvalues(self):
        # Get values from the entry boxes and return a dictionary of floats
        values = {}
        for fieldname, entrybox in self.ent.items():
            try:
                values[fieldname] = float(entrybox.get())
            except:
                # if the entry box is empty or not a number, use zero instead
                values[fieldname] = 0
                # display zero in the entry box
                entrybox.delete(0, tk.END)
                entrybox.insert(0, '0')

        # Assign the values to instance attributes
        self.vessel.pExt = values['External pressure']
        self.vessel.pInt = values['Internal pressure']
        self.vessel.OD = values['Outer diameter']
        self.vessel.ID = values['Inner diameter']
        self.vessel.yieldstress = values['Yield stress']
        self.vessel.deratedyieldstress = values['Derated Yield (400F)']

    def update_results(self):
        self.get_entryvalues()
        self.vessel.calculate()

        # Check the safety factors, and select the display color
        if self.vessel.SF_room < 1.00:
            roomcolor = '#ff8888'
        else:
            roomcolor = '#02BC94'

        if self.vessel.SF_derated < 1.00:
            deratedcolor = '#ff8888'
        else:
            deratedcolor = '#02BC94'

        # Get the new results and display them in the output table
        self.outputs['Average Linear Stress']['calculated'].configure(
                text='{:,.1f}'.format(self.vessel.averagestress))
        self.outputs['Average Linear Stress']['room'].configure(
                text='{:,.0f}'.format(self.vessel.yieldstress*self.vessel.k))
        self.outputs['Average Linear Stress']['derated'].configure(
                text='{:,.0f}'.format(self.vessel.deratedyieldstress*self.vessel.k))

        self.outputs['Maximum Local Stress']['calculated'].configure(
                text='{:,.1f}'.format(self.vessel.maxstress))
        self.outputs['Maximum Local Stress']['room'].configure(
                text='{:,.0f}'.format(self.vessel.yieldstress))
        self.outputs['Maximum Local Stress']['derated'].configure(
                text='{:,.0f}'.format(self.vessel.deratedyieldstress))

        self.outputs['Minimum Safety Factor']['room'].configure(
                text='{:,.3f}'.format(self.vessel.SF_room),
                background=roomcolor,
                foreground='white')
        self.outputs['Minimum Safety Factor']['derated'].configure(
                text='{:,.3f}'.format(self.vessel.SF_derated),
                background=deratedcolor,
                foreground='white')

        self.outputs['Internal Pressure for Burst']['room'].configure(
                text='{:,.3f}'.format(self.vessel.maxIntroom))
        self.outputs['Internal Pressure for Burst']['derated'].configure(
                text='{:,.3f}'.format(self.vessel.maxIntderated))
        self.outputs['External Pressure for Collapse']['room'].configure(
                text='{:,.3f}'.format(self.vessel.maxExtroom))
        self.outputs['External Pressure for Collapse']['derated'].configure(
                text='{:,.3f}'.format(self.vessel.maxExtderated))


def check_diameters(vessel, new_ID, new_OD):
    """ Change the vessel's ID and OD and return the room temp safety factor.
    """
    if new_OD <= new_ID:
        # OD must be larger than ID by any finite amount
        # Otherwise, don't try calculating, may cause error
        return 0
    else:
        vessel.modify_parameters(ID=new_ID, OD=new_OD)
        return vessel.SF_room


def plot_range(ID_min, ID_max, OD_min, OD_max):
    """ Calculate the room-temperature safety factor for ID and OD pairs across
    the given ranges.
    """
    # Default increment for the diameters
    step_size = 0.005
    ID_values = np.arange(ID_min, ID_max + 0.005, step_size)
    OD_values = np.arange(OD_min, OD_max + 0.005, step_size)
    # Create a numpy-compatible function from the check_diameters() function
    vector_check_diameters = np.vectorize(check_diameters)
    # Initialize a vessel to use
    v = Vessel(15, 0, ID_min, OD_min, 120, 116)
    # Create a meshgrid of the diameter ranges, to calculate all combinations
    ID_grid, OD_grid = np.meshgrid(ID_values, OD_values)
    # Get the safety factors for all the combinations
    SF_grid = vector_check_diameters(v, ID_grid, OD_grid)
    # Plot the calculated safety factors as an image array
    plt.imshow(SF_grid, cmap=plt.cm.Blues, origin='lower',
               extent=(ID_min, ID_max, OD_min, OD_max))
    c = plt.contour(ID_grid, OD_grid, SF_grid, levels=[1], colors='k')
    plt.clabel(c)
    # Show plot
    plt.show()
