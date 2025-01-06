import tkinter as tk
from app.models.timer import *

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Show Timer")
        self.root.geometry("800x500")
        self.default_bg = self.root.cget("bg")

        # Please change to be your show name
        self.show_name = ""

        # Settings
        self.inteveral_time = 900
        self.calls = [["Quarter", 900],["Five", 300],["Beginners", 300]]
        self.call_timers = []
        self.interval_over = False

        self.current_call = 0 
        # Initilise Timers
        self.form = formatter()
        self.running_time_timer = Stopwatch()
        self.show_stop_timer = Stopwatch()
        self.inteveral_timer = Timer(self.inteveral_time, False)
        self.act_2_begginers = Timer((self.inteveral_time - 300), True)
        
        for name, duration in self.calls:
            newCallTimer = Timer(duration, True)
            self.call_timers.append(newCallTimer)

        self.localtime = LocalTime()

        # Allows to track when
        self.act_1_start = None
        self.act_1_end = None

        self.act_2_start = None
        self.act_2_end = None

        self.interval_start = None
        self.interval_End = None

        # Goto pre show page
        self.preShow()

    def clearWindow(self):
        for item in self.root.winfo_children():
            item.destroy()

    # Windows
    def preShow(self): # Screen for before the show (call timers, local time etc.)
        self.clearWindow()

        def update_cue_timer():
            # Place here any functions that must update with the screen
            if self.call_timers[self.current_call - 1]._remaining_time < 0:
                self.current_call_timer_label.config(text="00:00:00")
            
            elif self.is_calls_visible:
                self.current_call_timer_label.config(text=(self.call_timers[self.current_call - 1].get_time()))

            self.preShow_tasks.append(self.root.after(10, update_cue_timer))

        def update_local_timer():
            # Local Timer Update
            self.local_timer_label.config(text=f"{self.localtime.get_time()}")

            self.preShow_tasks.append(self.root.after(1000, update_local_timer))

        def startShowCalls():
            self.is_calls_visible = True
            if self.current_call < len(self.calls):
                # Updating Next Call Text
                try:
                    call_name, call_time = self.calls[self.current_call + 1]
                    self.next_call_label.config(text=f"Next Call: {call_name} - {call_time / 60} Mins")
                except IndexError:
                    self.next_call_label.config(text=f"Next Call:")

                # Start and update timer
                try:
                    self.current_call_label.config(text=f'Current Call: {self.calls[self.current_call][0]}')
                    self.current_call_timer_label.config(text=(self.call_timers[self.current_call].get_time()), font=("Helvetica", 36))
                    self.call_timers[self.current_call].start()
                except IndexError:
                    self.next_call_label.config(text="Current Call: No Calls Remaining.")
                update_cue_timer()
                self.current_call += 1
            else:
                self.current_call_label.config(text="Next Call: No Calls Remaining.")
                self.current_call_timer_label.config(text="", font=("Helvetica", 0))
                self.is_calls_visible = False

        def changeToMain(): 
            self.localtime.stop()

            self.act_1_start = time.localtime()

            for task in self.preShow_tasks: # Stops anything in the task queue.

                self.root.after_cancel(task)
                task = None

            for allTimers in self.call_timers: # Cancel Any Running Timers
                if allTimers.get_running():
                    allTimers.stop()
            
            self.clearWindow()
            self.mainShowWindow()

        self.preShow_tasks = []

        self.call_frame = tk.Frame(self.root)
        self.call_frame.pack(fill='x')

        self.is_calls_visible = False
        self.show_call_button = tk.Button(self.call_frame, text="Next Show Call", font=("Helvetica", 14), width=15, command=startShowCalls,
                                          relief="solid", borderwidth=2, fg="black", bg="white", activeforeground="black", activebackground="white")
        self.show_call_button.pack(side="top", pady=10)

        self.next_call_label = tk.Label(self.call_frame, text=f"Next Call: {self.calls[0][0]} - {self.calls[0][1] / 60} Mins", fg="lightgrey",font=("Helvetica", 14))
        self.next_call_label.pack()

        self.current_call_label = tk.Label(self.call_frame, text="Current Call:", font=("Helvetica", 16))
        self.current_call_label.pack(pady=2)

        self.current_call_timer_label = tk.Label(self.call_frame, text="", font=("Helvetica", 0), fg="lightgrey")
        self.current_call_timer_label.pack(pady=0)

        # Center Lavel and Global Timer

        self.center_frame = tk.Frame(self.root)
        self.center_frame.place(relx=0.5, rely=0.5, anchor='center')

        self.title_label = tk.Label(self.center_frame, text="Show Timer", font=('Helvetica', 48))
        self.title_label.pack(pady=(0,5))

        self.local_timer_label = tk.Label(self.center_frame, text="00:00:00", font=("Helvetica", 42), fg='lightgrey')
        self.local_timer_label.pack()

        self.start_show_button = tk.Button(self.root, text="Start Show", font=("Helvetica", 14), width=15, command=changeToMain)
        self.start_show_button.pack(side='bottom', pady=20)
        
        self.localtime.start()
        update_local_timer()

    
    def mainShowWindow(self):
        # Code to start main show timer
        self.mainShowTasks = []

        self.root.update_idletasks()

        self.running_time_timer.start()
        self.localtime.start()

        def update_ShowStop():
            self.stopped_timer_label.config(text=(self.show_stop_timer.get_time()), font=("Helvetica", 36, "bold"))
            self.mainShowTasks.append(self.root.after(10, update_ShowStop))

        def update_mainTimer():
            self.main_running_timer_label.config(text=self.running_time_timer.get_time())
            self.mainShowTasks.append(self.root.after(10, update_mainTimer))

        def update_localTime():
            self.local_timer_label.config(text=self.localtime.get_time())
            self.mainShowTasks.append(self.root.after(1000, update_localTime))

        def toggleShowStop():
            if  not self.show_stop_timer.get_running():
                self.show_stop_timer.start()
                self.show_stop_button.config(text="End Show Stop")
                update_ShowStop()
            else:
                self.show_stop_timer.stop()
                self.show_stop_button.config(text="Show Stop")
            
            
        def goToInterval():
            self.show_stop_timer.stop()

            self.interval_start = self.act_1_end = time.localtime()
            

            for task in self.mainShowTasks:
                self.root.after_cancel(task)
                task = None
            
            self.clearWindow()
            self.root.update_idletasks()
            self.intervalView()
            # There is no need to stop timers as most must stay running while the show is running.

        def endshow():
            self.act_2_end = time.localtime()
            self.running_time_timer.stop()
            self.show_stop_timer.stop()
            self.localtime.stop()

            for task in self.mainShowTasks:
                self.root.after_cancel(task)
                task = None
            
            self.clearWindow()
            self.root.update_idletasks()
            self.showInsights()

        self.show_stop_button = tk.Button(self.root, text="Show Stop", font=("Helvetica", 14), width=15, command=toggleShowStop,
                                          relief="solid", borderwidth=2, fg="red", bg="black", activeforeground="red", activebackground="black")
        self.show_stop_button.pack(side="top", pady=10)

        self.mainframe = tk.Frame(self.root)
        self.mainframe.pack(expand=True)

        # Center Timers
        self.stopped_timer_label = tk.Label(self.mainframe, font=("Helvetica", 0, "bold"), text="", fg="#D32F2F") 
        self.stopped_timer_label.pack(side="top", pady=5)

        self.main_running_timer_label = tk.Label(self.mainframe, font=("Helvetica", 48, "bold"), text="00:00:00:00")
        self.main_running_timer_label.pack(pady=(0, 5))

        self.local_timer_label = tk.Label(self.mainframe, font=("Helvetica", 42), text="00:00:00", fg="lightgrey")
        self.local_timer_label.pack()

        # Show Interval Screen
        if not self.interval_over:
            self.actdown_button = tk.Button(self.root, text="Act Down", font=("Helvetica", 14), width=15, command=goToInterval)
            self.actdown_button.pack(side="bottom", pady=20)
        elif self.interval_over:
            self.actdown_button = tk.Button(self.root, text="End Show", font=("Helvetica", 14), width=15, command=endshow)
            self.actdown_button.pack(side="bottom", pady=20)
        
        update_mainTimer()
        update_localTime()

            
    def intervalView(self):

        self.interval_tasks = []
        # Initilise timers and change vars
        self.interval_over = True
        self.inteveral_timer.start()
        self.act_2_begginers.start()
        

        def update_timers(): # Becuase all are on 1 second counts and dont stop
            self.begginers_time_label.config(text=self.act_2_begginers.get_time())
            self.interval_countdown_lable.config(text=self.inteveral_timer.get_time())
            self.local_timer_label.config(text=self.localtime.get_time())

            # Function to update screen colour if timer approches 0
            time_left = self.inteveral_timer.get_remaining_time()
            if time_left <= 300 and time_left > 0:
                self.root.config(bg="#FFA500")
            elif time_left <= 0:
                self.root.config(bg="red")


            self.interval_tasks.append(self.root.after(1000, update_timers))

        def end_interval():
            self.interval_End = self.act_2_start = time.localtime()
            self.root.config(bg=self.default_bg)

            for task in self.interval_tasks:
                self.root.after_cancel(task)
                task = None
            
            self.clearWindow()
            self.root.update_idletasks()
            self.mainShowWindow()

        self.begginers_label = tk.Label(self.root, text="Begginers", font=("Helvetica", 16), fg="lightgrey")
        self.begginers_label.pack(pady=5)

        self.begginers_time_label = tk.Label(self.root, text=f"{self.act_2_begginers.get_time()}", font=("Helvetica", 14), fg="lightgrey")
        self.begginers_time_label.pack(pady=2)

        self.frame = tk.Frame(self.root)
        self.frame.place(relx=0.5, rely=0.5, anchor="center")

        self.interval_countdown_lable = tk.Label(self.frame, text="00:00:00", font=("Helvetica", 48))
        self.interval_countdown_lable.pack(pady=(0,5))
        
        self.local_timer_label = tk.Label(self.frame, text="00:00:00", font=("Helvetica", 42), fg="lightgrey")
        self.local_timer_label.pack()

        
        # Back to main show 
        self.end_interval_button = tk.Button(self.root, text="End Interval", font=("Helvetica", 14), width=15, command=end_interval)
        self.end_interval_button.pack(side='bottom', pady=20)
        update_timers()


    def showInsights(self):

        def saveToJSON():
            import json, os

            filename = f"app/userdata/{self.show_name}.json"

            if os.path.exists(filename):
                with open(filename, "r") as json_file:
                    show_data = json.load(json_file)
            
            else:
                show_data = {}

            next_show_key = f"Show{len(show_data) + 1}"

            new_show_data = {
                "act_1" : {
                    "start" : f"{time.strftime("%H:%M:%S", self.act_1_start)}",
                    "end" : f"{time.strftime("%H:%M:%S", self.act_1_end)}",
                    "running_time" : f"{self.form.delta_time(self.act_1_start, self.act_1_end)}"
                },

                "interval" : {
                    "start" : f"{time.strftime("%H:%M:%S", self.interval_start)}",
                    "end" : f"{time.strftime("%H:%M:%S", self.interval_End)}",
                    "running_time" : f"{self.form.delta_time(self.interval_start, self.interval_End)}"
                },

                "act_2" : {
                    "start" : f"{time.strftime("%H:%M:%S", self.act_2_start)}",
                    "end" : f"{time.strftime("%H:%M:%S", self.act_2_end)}",
                    "running_time" : f"{self.form.delta_time(self.act_2_start, self.act_2_end)}"
                },

                "show_details" : {
                    "total_running_time" : f"{self.running_time_timer.get_time()}",
                    "show_stopped" : f"{self.show_stop_timer.get_time()}",
                    "stage_time" : f"{self.form.format_secs((time.mktime(self.act_1_end) - time.mktime(self.act_1_start)) + (time.mktime(self.act_2_end) - time.mktime(self.act_2_start)))}"
                }
            }

            show_data[next_show_key] = new_show_data

            with open(filename, "w") as json_file:
                json.dump(show_data, json_file, indent=4)

            print(f"Show Saved To {filename}, under {next_show_key}.")
            startNewShow() # To prevent saving twice.

        def startNewShow():
            self.clearWindow()

            # Re init all vars needed.
            # Settings
            self.inteveral_time = 900
            self.calls = [["Quarter", 900],["Five", 300],["Beginners", 300]]
            self.call_timers = []
            self.interval_over = False

            self.current_call = 0 
            # Initilise Timers
            self.form = formatter()
            self.running_time_timer = Stopwatch()
            self.show_stop_timer = Stopwatch()
            self.inteveral_timer = Timer(self.inteveral_time, False)
            self.act_2_begginers = Timer((self.inteveral_time - 300), True)
            
            for name, duration in self.calls:
                newCallTimer = Timer(duration, True)
                self.call_timers.append(newCallTimer)

            self.localtime = LocalTime()

            # Allows to track when
            self.act_1_start = None
            self.act_1_end = None

            self.act_2_start = None
            self.act_2_end = None

            self.interval_start = None
            self.interval_End = None

            # Goto pre show page
            self.preShow()

        self.insight_headder_lable = tk.Label(self.root, text="Show Insights", font=("Helvetica", 36, "bold"))
        self.insight_headder_lable.pack(side="top", pady=5)

        self.Act1_label = tk.Label(self.root, text="Act 1:", font=("Helvetica", 24))
        self.Act1_label.pack(anchor='w', padx=20)

        self.act1_details_labels = tk.Label(self.root, text=f"Start: {time.strftime("%H:%M:%S", self.act_1_start)} | End: {time.strftime("%H:%M:%S", self.act_1_end)} \n {self.form.delta_time(self.act_1_start, self.act_1_end)}",
                                             font=("Helvetica", 20))
        self.act1_details_labels.pack(anchor='center', padx=40)

        self.interval_label = tk.Label(self.root, text="Interval:", font=("Helvetica", 24))
        self.interval_label.pack(anchor='w', padx=20)

        self.interval_details_label = tk.Label(self.root, text=f"Start: {time.strftime("%H:%M:%S", self.interval_start)} | End: {time.strftime("%H:%M:%S", self.interval_End)} \n {self.form.delta_time(self.interval_start, self.interval_End)}",
                                               font=("Helvetica", 20))
        self.interval_details_label.pack(anchor='center', padx=40)


        self.Act2_label = tk.Label(self.root, text="Act 2:", font=("Helvetica", 24))
        self.Act2_label.pack(anchor='w', padx=20)

        self.act2_details_labels = tk.Label(self.root, text=f"Start: {time.strftime("%H:%M:%S", self.act_2_start)} | End: {time.strftime("%H:%M:%S", self.act_2_end)} \n {self.form.delta_time(self.act_2_start, self.act_2_end)}",
                                            font=("Helvetica", 20))
        self.act2_details_labels.pack(anchor='center', padx=40)

        self.divider = tk.Frame(self.root, height=1, bg='lightgrey')
        self.divider.pack(fill='x', padx=20, pady=10)

        self.show_total_time_label = tk.Label(self.root, text=f"Total Running Time: {self.running_time_timer.get_time()}", font=("Helvetica", 20))
        self.show_total_time_label.pack(anchor='center')

        self.show_stop_time_lable = tk.Label(self.root, text=f'Show Stopped Time: {self.show_stop_timer.get_time()}', font=("Helvetica", 20))
        self.show_stop_time_lable.pack(anchor='center')

        button_frame = tk.Frame(self.root)
        button_frame.pack(side="bottom", pady=10)

        # Save to JSON Button
        self.save_to_system_button = tk.Button(
            button_frame, 
            text="Save to JSON", 
            font=("Helvetica", 14), 
            width=15, 
            command=saveToJSON
        )
        self.save_to_system_button.grid(column=0, row=0, padx=5)

        # Start New Show Button
        self.new_show_button = tk.Button(
            button_frame, 
            text="Start New Show", 
            font=("Helvetica", 14), 
            width=15, 
            command=startNewShow
        )
        self.new_show_button.grid(column=1, row=0, padx=5)