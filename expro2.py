import ttkbootstrap as tk
import tkinter.ttk as ttk
from ttkbootstrap.constants import *
from tkinter import font as tkfont
import datetime
import json
import statistics


FONT_1 = ('Verdana', 35)
FONT_2 = ('Arial', 20)

today = datetime.date.today()
exam_date = datetime.date(2024, 5, 13)

diff = exam_date - today
days_left = diff.days

# gen_progress
settings = {
    'general-progress': 0,
    'mts-progress': 0,
    'phy-progress': 0,
    'mee-progress': 0,
    'bio-progress': 0,
    'gns1-progress': 0,
    'gns3-progress': 0,
    'che-progress': 0,
    'mts': {
        'sec-a': 30,
        'sec-b': 0,
        'sec-c': 0,
        'sec-d': 0,
        'sec-e': 0,
        'sec-f': 0,
        'sec-g': 0,
    },
    'phy': {
        'um': 0,
        'vs': 0,
        'ki': 0,
        'wp': 0,
        'pr': 0,
        'mw': 0,
        'nw': 0,
        'sd': 0,
        'rm': 0,
    }, 
    'mee': {
        'ge': 0,
        'po': 0,
        'ta': 0,
        'lo': 0,
        'pp': 0,
        'op': 0,
        'fs': 0,
    },
    'bio': {
        'bi': 0,
        'ec': 0,
        'ce': 0, 
        're': 0,
        'va': 0,
        'bp': 0,
        'af': 0,
        'vf': 0,
    },
    'gns1': {
        'tm': 0,
        'ss': 0,
        'wf': 0,
        'ps': 0,
        'nt': 0,
    },
    'gns3': {
        'c12': 0,
        'c34': 0,
        'c56': 0,
        'c78': 0
    },
    'che': {
        'at': 0,
        'ea': 0,
        'ce': 0,
        'ck': 0,
        'tc': 0,
        'ec': 0,
        'ra': 0,
        'sl': 0,
    }

}

def update():
    settings['mts-progress'] = statistics.mean([settings['mts']['sec-a'], settings['mts']['sec-b'], settings['mts']['sec-c'], settings['mts']['sec-d'], settings['mts']['sec-e'], settings['mts']['sec-f'], settings['mts']['sec-g']])
    settings['general-progress'] = (settings['mts-progress'] + settings['phy-progress'] + settings['mee-progress'] + settings['bio-progress'] + settings['gns1-progress'] + settings['gns3-progress'] + settings['che-progress']) / 7
    settings['mee-progress'] = statistics.mean([settings['mee']['ge'], settings['mee']['po'], settings['mee']['ta'], settings['mee']['lo'], settings['mee']['pp'], settings['mee']['op'], settings['mee']['fs']])
    settings['phy-progress'] = statistics.mean([settings['phy']['um'], settings['phy']['vs'], settings['phy']['ki'], settings['phy']['wp'], settings['phy']['pr'], settings['phy']['mw'], settings['phy']['nw'], settings['phy']['sd'], settings['phy']['rm']])
    settings['bio-progress'] = statistics.mean([settings['bio']['bi'], settings['bio']['ec'], settings['bio']['ce'], settings['bio']['re'], settings['bio']['va'], settings['bio']['bp'], settings['bio']['af'], settings['bio']['vf']])
    settings['gns1-progress'] = statistics.mean([settings['gns1']['tm'], settings['gns1']['ss'], settings['gns1']['wf'], settings['gns1']['ps'], settings['gns1']['nt']])
    settings['gns3-progress'] = statistics.mean([settings['gns3']['c12'], settings['gns3']['c34'], settings['gns3']['c56'], settings['gns3']['c78']])
    settings['che-progress'] = statistics.mean([settings['che']['at'], settings['che']['ea'], settings['che']['ce'], settings['che']['ck'], settings['che']['tc'], settings['che']['ec'], settings['che']['ra'], settings['che']['sl']])


def save():
    update()
    with open('settings.json', 'w') as s:
        json.dump(settings, s)
        s.close()
   
# save()
with open('settings.json', 'r') as s:
    data = s.read()
    data = json.loads(data)
    print(data)
    settings = data


def modify(entry, probar, v1, v2):
        no = entry.get()
        print(no)
        cur_bar = probar['value']
        if cur_bar < 0:
            cur_bar = 0
        cur_bar = int(no) + int(cur_bar)
        probar['value'] = cur_bar
        # print('f v: ' + str(value))
        # value = cur_bar
        # print(value)
        settings[v1][v2] = cur_bar
        save()
        

save()

class App(tk.Window):
    def __init__(self, *args, **kwargs):
        tk.Window.__init__(self, *args, **kwargs)
        style = tk.Style('superhero')
        container = tk.Frame(self)
        container.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=2)
        self.geometry('800x700')
        self.title('ExPro')
        self.title_font = tkfont.Font(family='Helvrtica', size=18)

        self.frames = {}
        for F in (MainPage, MTS, PHY, MEE, BIO, GNS1, GNS3, CHE):
            page_name =  F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0)

        self.show_frame('MainPage')

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, width=670, height=620)
        self.controller = controller

        self.main_frame = tk.Frame(self, width=670, height=500)
        self.main_frame.place(x=0, y=0)

        self.label = tk.Label(self.main_frame, text=f"{days_left} days left to EXAM", font=FONT_1)
        self.label.grid(row=0, column=0, columnspan=3, pady=10)

        self.von = 3

        self.gen_progressbar = tk.Progressbar(self.main_frame, maximum=100, value=settings['general-progress'], length=600)
        self.gen_progressbar.grid(row=1, column=0, columnspan=3, pady=(0, 5))

        self.gen_guage = tk.Meter(self.main_frame, metersize=100, amounttotal=100, amountused=round(int(settings['general-progress']), 2))
        self.gen_guage.grid(row=1, column=1, columnspan=3, pady=(0, 5))

        frame_style = LIGHT
        btn_style = OUTLINE
        self.mts_frame = tk.Frame(self.main_frame, width=20, height=10, style=frame_style)
        self.mts_frame.grid(row=2, column=0, padx=(10, 0))
        self.mts_label = tk.Label(self.mts_frame, text="MTS 101", font=FONT_2, background='')
        self.mts_label.pack(pady=10)
        self.mts_progressbar = tk.Progressbar(self.mts_frame, maximum=100, value=settings['mts-progress'], length=200)
        self.mts_progressbar.pack(padx=5)
        self.mts_button = tk.Button(self.mts_frame, text='Progress', style=btn_style, command=lambda: controller.show_frame('MTS'))
        self.mts_button.pack(pady=10)

        self.phy101_frame = tk.Frame(self.main_frame, width=20, height=10, style=frame_style)
        self.phy101_frame.grid(row=2, column=1, padx=10)
        self.phy101_label = tk.Label(self.phy101_frame, text="PHY 101", font=FONT_2)
        self.phy101_label.pack(pady=10)
        self.phy101_progressbar = tk.Progressbar(self.phy101_frame, maximum=100, value=settings['phy-progress'], length=200)
        self.phy101_progressbar.pack(padx=5)
        self.phy101_button = tk.Button(self.phy101_frame, text='Progress', style=btn_style, command=lambda: controller.show_frame('PHY'))
        self.phy101_button.pack(pady=10)

        self.mee101_frame = tk.Frame(self.main_frame, width=20, height=10, style=frame_style)
        self.mee101_frame.grid(row=2, column=2, padx=(0, 10))
        self.mee101_label = tk.Label(self.mee101_frame, text="MEE 101", font=FONT_2)
        self.mee101_label.pack(pady=10)
        self.mee101_progressbar = tk.Progressbar(self.mee101_frame, maximum=100, value=settings['mee-progress'], length=200)
        self.mee101_progressbar.pack(padx=5)
        self.mee101_button = tk.Button(self.mee101_frame, text='Progress', style=btn_style, command=lambda: controller.show_frame('MEE'))
        self.mee101_button.pack(pady=10)

        
        self.bio101_frame = tk.Frame(self.main_frame, width=20, height=10, style=frame_style)
        self.bio101_frame.grid(row=3, column=0, padx=(10, 0), pady=10)
        self.bio101_label = tk.Label(self.bio101_frame, text="BIO 101", font=FONT_2)
        self.bio101_label.pack(pady=10)
        self.bio101_progressbar = tk.Progressbar(self.bio101_frame, maximum=100, value=settings['bio-progress'], length=200)
        self.bio101_progressbar.pack(padx=5)
        self.bio101_button = tk.Button(self.bio101_frame, text='Progress', style=btn_style, command=lambda: controller.show_frame('BIO'))
        self.bio101_button.pack(pady=10)

        self.gns101_frame = tk.Frame(self.main_frame, width=20, height=10, style=frame_style)
        self.gns101_frame.grid(row=3, column=1, padx=10, pady=10)
        self.gns101_label = tk.Label(self.gns101_frame, text="GNS 101", font=FONT_2)
        self.gns101_label.pack(pady=10)
        self.gns101_progressbar = tk.Progressbar(self.gns101_frame, maximum=100, value=settings['gns1-progress'], length=200)
        self.gns101_progressbar.pack(padx=5)
        self.gns101_button = tk.Button(self.gns101_frame, text='Progress', style=btn_style,command=lambda: controller.show_frame('GNS1'))
        self.gns101_button.pack(pady=10)

        self.gns103_frame = tk.Frame(self.main_frame, width=20, height=10, style=frame_style)
        self.gns103_frame.grid(row=3, column=2, padx=(0, 10), pady=10)
        self.gns103_label = tk.Label(self.gns103_frame, text="GNS 103", font=FONT_2)
        self.gns103_label.pack(pady=10)
        self.gns103_progressbar = tk.Progressbar(self.gns103_frame, maximum=100, value=settings['gns3-progress'], length=200)
        self.gns103_progressbar.pack(padx=5)
        self.gns103_button = tk.Button(self.gns103_frame, text='Progress',style=btn_style, command=lambda: controller.show_frame('GNS3'))
        self.gns103_button.pack(pady=10)

        self.che101_frame = tk.Frame(self.main_frame, width=20, height=10, style=frame_style)
        self.che101_frame.grid(row=4, column=1, padx=10, pady=10)
        self.che101_label = tk.Label(self.che101_frame, text="CHE 101", font=FONT_2)
        self.che101_label.pack(pady=10)
        self.che101_progressbar = tk.Progressbar(self.che101_frame, maximum=100, value=settings['che-progress'], length=200)
        self.che101_progressbar.pack(padx=5)
        self.che101_button = tk.Button(self.che101_frame, text='Progress', style=btn_style, command=lambda: controller.show_frame('CHE'))
        self.che101_button.pack(pady=10)


class MTS(tk.Frame):
    def __init__(self, parent, controller):
        # MainPage(self, controller=self).destroy()
        tk.Frame.__init__(self, parent, width=675, height=500)
        self.controller = controller

        main_frame = tk.Frame(self, width=700, height=500)
        main_frame.place(x=0, y=0, relx=0, rely=0)
        
        label = tk.Label(main_frame, text='MTS Progress Page', font=FONT_1)
        label.pack(side=tk.TOP, fill=tk.X, pady=10, anchor=tk.CENTER)

        mts_progress = tk.Progressbar(main_frame, value=settings['mts-progress'], maximum=100, length=450)
        mts_progress.pack()

 
        prog_frame = tk.Frame(main_frame)
        prog_frame.pack()

        a_label = tk.Label(prog_frame, text='A - SET .TH', font=FONT_2)
        a_label.grid(row=0, column=0)
        a_pro = tk.Progressbar(prog_frame, value=settings['mts']['sec-a'], length=200, maximum=100)
        a_pro.grid(row=0, column=1, padx=10)
        a_entry = tk.Entry(prog_frame, width=5)
        a_entry.grid(row=0, column=2)
        a_modify = tk.Button(prog_frame, text='mod', command=lambda: modify(a_entry, a_pro, 'mts', 'sec-a'))
        a_modify.grid(row=0, column=3, padx=10)

        b_label = tk.Label(prog_frame, text='B - R .MI', font=FONT_2)
        b_label.grid(row=1, column=0)
        b_pro = tk.Progressbar(prog_frame, value=settings['mts']['sec-b'], length=200, maximum=100)
        b_pro.grid(row=1, column=1, padx=10)
        b_entry = tk.Entry(prog_frame, width=5)
        b_entry.grid(row=1, column=2)
        b_modify = tk.Button(prog_frame, text='mod', command=lambda: modify(b_entry, b_pro, 'mts', 'sec-b'))
        b_modify.grid(row=1, column=3, padx=10)

        c_label = tk.Label(prog_frame, text='C - Seq. Ser', font=FONT_2)
        c_label.grid(row=2, column=0)
        c_pro = tk.Progressbar(prog_frame, value=settings['mts']['sec-c'], length=200, maximum=100)
        c_pro.grid(row=2, column=1, padx=10)
        c_entry = tk.Entry(prog_frame, width=5)
        c_entry.grid(row=2, column=2)
        c_modify = tk.Button(prog_frame, text='mod', command=lambda: modify(c_entry, c_pro, 'mts','sec-c'))
        c_modify.grid(row=2, column=3, padx=10)

        d_label = tk.Label(prog_frame, text='D - Qua .Eq', font=FONT_2)
        d_label.grid(row=3, column=0)
        d_pro = tk.Progressbar(prog_frame, value=settings['mts']['sec-d'], length=200, maximum=100)
        d_pro.grid(row=3, column=1, padx=10)
        d_entry = tk.Entry(prog_frame, width=5)
        d_entry.grid(row=3, column=2)
        d_modify = tk.Button(prog_frame, text='mod', command=lambda: modify(d_entry, d_pro, 'mts','sec-d'))
        d_modify.grid(row=3, column=3, padx=10)

        e_label = tk.Label(prog_frame, text='E - Bin .Th', font=FONT_2)
        e_label.grid(row=4, column=0)
        e_pro = tk.Progressbar(prog_frame, value=settings['mts']['sec-e'], length=200, maximum=100)
        e_pro.grid(row=4, column=1, padx=10)
        e_entry = tk.Entry(prog_frame, width=5)
        e_entry.grid(row=4, column=2)
        e_modify = tk.Button(prog_frame, text='mod', command=lambda: modify(e_entry, e_pro, 'mts','sec-e'))
        e_modify.grid(row=4, column=3, padx=10)

        f_label = tk.Label(prog_frame, text='F - Cir .Me', font=FONT_2)
        f_label.grid(row=5, column=0)
        f_pro = tk.Progressbar(prog_frame, value=settings['mts']['sec-f'], length=200, maximum=100)
        f_pro.grid(row=5, column=1, padx=10)
        f_entry = tk.Entry(prog_frame, width=5)
        f_entry.grid(row=5, column=2)
        f_modify = tk.Button(prog_frame, text='mod', command=lambda: modify(f_entry, f_pro, 'mts','sec-f'))
        f_modify.grid(row=5, column=3, padx=10)

        g_label = tk.Label(prog_frame, text='G - Tri .Fu', font=FONT_2)
        g_label.grid(row=6, column=0)
        g_pro = tk.Progressbar(prog_frame, value=settings['mts']['sec-g'], length=200, maximum=100)
        g_pro.grid(row=6, column=1, padx=10)
        g_entry = tk.Entry(prog_frame, width=5)
        g_entry.grid(row=6, column=2)
        g_modify = tk.Button(prog_frame, text='mod', command=lambda: modify(g_entry, g_pro, 'mts','sec-g'))
        g_modify.grid(row=6, column=3, padx=10)

        main_button = tk.Button(main_frame, text='Main Page', command=lambda: controller.show_frame('MainPage'))
        main_button.pack(pady=10)


class PHY(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, width=675, height=500)
        self.controller = controller

        main_frame = tk.Frame(self, width=700, height=500)
        main_frame.place(x=0, y=0, relx=0, rely=0)
        
        label = tk.Label(main_frame, text='PHY 101 Progress Page', font=FONT_1)
        label.pack(side=tk.TOP, fill=tk.X, pady=10, anchor=tk.CENTER)

        phy_progress = tk.Progressbar(main_frame, value=settings['phy-progress'], maximum=100, length=450)
        phy_progress.pack()


 
        prog_frame = tk.Frame(main_frame)
        prog_frame.pack()

        um_label = tk.Label(prog_frame, text='Unit .Mea', font=FONT_2)
        um_label.grid(row=0, column=0)
        um_pro = tk.Progressbar(prog_frame, value=settings['phy']['um'], length=200, maximum=100)
        um_pro.grid(row=0, column=1, padx=10)
        um_entry = tk.Entry(prog_frame, width=5)
        um_entry.grid(row=0, column=2)
        um_modify = tk.Button(prog_frame, text='mod', command=lambda: modify(um_entry, um_pro, 'phy', 'um'))
        um_modify.grid(row=0, column=3, padx=10)

        vs_label = tk.Label(prog_frame, text='Vector .S', font=FONT_2)
        vs_label.grid(row=1, column=0)
        vs_pro = tk.Progressbar(prog_frame, value=settings['phy']['vs'], length=200, maximum=100)
        vs_pro.grid(row=1, column=1, padx=10)
        vs_entry = tk.Entry(prog_frame, width=5)
        vs_entry.grid(row=1, column=2)
        vs_modify = tk.Button(prog_frame, text='mod', command=lambda: modify(vs_entry, vs_pro, 'phy', 'vs'))
        vs_modify.grid(row=1, column=3, padx=10)

        ki_label = tk.Label(prog_frame, text='Kinematics', font=FONT_2)
        ki_label.grid(row=2, column=0)
        ki_pro = tk.Progressbar(prog_frame, value=settings['phy']['ki'], length=200, maximum=100)
        ki_pro.grid(row=2, column=1, padx=10)
        ki_entry = tk.Entry(prog_frame, width=5)
        ki_entry.grid(row=2, column=2)
        ki_modify = tk.Button(prog_frame, text='mod', command=lambda: modify(ki_entry, ki_pro, 'phy', 'ki'))
        ki_modify.grid(row=2, column=3, padx=10)

        wp_label = tk.Label(prog_frame, text='Work .P', font=FONT_2)
        wp_label.grid(row=3, column=0)
        wp_pro = tk.Progressbar(prog_frame, value=settings['phy']['wp'], length=200, maximum=100)
        wp_pro.grid(row=3, column=1, padx=10)
        wp_entry = tk.Entry(prog_frame, width=5)
        wp_entry.grid(row=3, column=2)
        wp_modify = tk.Button(prog_frame, text='mod', command=lambda: modify(wp_entry, wp_pro, 'phy', 'wp'))
        wp_modify.grid(row=3, column=3, padx=10)

        pr_label = tk.Label(prog_frame, text='Projectile', font=FONT_2)
        pr_label.grid(row=4, column=0)
        pr_pro = tk.Progressbar(prog_frame, value=settings['phy']['pr'], length=200, maximum=100)
        pr_pro.grid(row=4, column=1, padx=10)
        pr_entry = tk.Entry(prog_frame, width=5)
        pr_entry.grid(row=4, column=2)
        pr_modify = tk.Button(prog_frame, text='mod', command=lambda: modify(pr_entry, pr_pro, 'phy', 'pr'))
        pr_modify.grid(row=4, column=3, padx=10)

        mw_label = tk.Label(prog_frame, text='Mass .W', font=FONT_2)
        mw_label.grid(row=5, column=0)
        mw_pro = tk.Progressbar(prog_frame, value=settings['phy']['mw'], length=200, maximum=100)
        mw_pro.grid(row=5, column=1, padx=10)
        mw_entry = tk.Entry(prog_frame, width=5)
        mw_entry.grid(row=5, column=2)
        mw_modify = tk.Button(prog_frame, text='mod', command=lambda: modify(mw_entry, mw_pro, 'phy', 'mw'))
        mw_modify.grid(row=5, column=3, padx=10)

        nm_label = tk.Label(prog_frame, text='Newton .M', font=FONT_2)
        nm_label.grid(row=6, column=0)
        nm_pro = tk.Progressbar(prog_frame, value=settings['phy']['nw'], length=200, maximum=100)
        nm_pro.grid(row=6, column=1, padx=10)
        nm_entry = tk.Entry(prog_frame, width=5)
        nm_entry.grid(row=6, column=2)
        nm_modify = tk.Button(prog_frame, text='mod', command=lambda: modify(nm_entry, nm_pro, 'phy', 'nw'))
        nm_modify.grid(row=6, column=3, padx=10)

        sd_label = tk.Label(prog_frame, text='Static .Dy', font=FONT_2)
        sd_label.grid(row=7, column=0)
        sd_pro = tk.Progressbar(prog_frame, value=settings['phy']['sd'], length=200, maximum=100)
        sd_pro.grid(row=7, column=1, padx=10)
        sd_entry = tk.Entry(prog_frame, width=5)
        sd_entry.grid(row=7, column=2)
        sd_modify = tk.Button(prog_frame, text='mod', command=lambda: modify(sd_entry, sd_pro, 'phy', 'sd'))
        sd_modify.grid(row=7, column=3, padx=10)

        rm_label = tk.Label(prog_frame, text='Rotaional .M', font=FONT_2)
        rm_label.grid(row=8, column=0)
        rm_pro = tk.Progressbar(prog_frame, value=settings['phy']['rm'], length=200, maximum=100)
        rm_pro.grid(row=8, column=1, padx=10)
        rm_entry = tk.Entry(prog_frame, width=5)
        rm_entry.grid(row=8, column=2)
        rm_modify = tk.Button(prog_frame, text='mod', command=lambda: modify(rm_entry, rm_pro, 'phy', 'rm'))
        rm_modify.grid(row=8, column=3, padx=10)

        main_button = tk.Button(main_frame, text='Main Page', command=lambda: controller.show_frame('MainPage'))
        main_button.pack(pady=10)


class MEE(tk.Frame):
    def __init__(self, parent, controller):
        # MainPage(self, controller=self).destroy()
        tk.Frame.__init__(self, parent, width=675, height=500)
        self.controller = controller

        main_frame = tk.Frame(self, width=700, height=500)
        main_frame.place(x=0, y=0, relx=0, rely=0)
        
        label = tk.Label(main_frame, text='MEE Progress Page', font=FONT_1)
        label.pack(side=tk.TOP, fill=tk.X, pady=10, anchor=tk.CENTER)

        mee_progress = tk.Progressbar(main_frame, value=settings['mee-progress'], maximum=100, length=450)
        mee_progress.pack()

 
        prog_frame = tk.Frame(main_frame)
        prog_frame.pack()

        ge_label = tk.Label(prog_frame, text='Geometrical .C', font=FONT_2)
        ge_label.grid(row=0, column=0)
        ge_pro = tk.Progressbar(prog_frame, value=settings['mee']['ge'], length=200, maximum=100)
        ge_pro.grid(row=0, column=1, padx=10)
        ge_entry = tk.Entry(prog_frame, width=5)
        ge_entry.grid(row=0, column=2)
        ge_modify = tk.Button(prog_frame, text='mod', command=lambda: modify(ge_entry, ge_pro, 'mee', 'ge'))
        ge_modify.grid(row=0, column=3, padx=10)

        po_label = tk.Label(prog_frame, text='Polygon', font=FONT_2)
        po_label.grid(row=1, column=0)
        po_pro = tk.Progressbar(prog_frame, value=settings['mee']['po'], length=200, maximum=100)
        po_pro.grid(row=1, column=1, padx=10)
        po_entry = tk.Entry(prog_frame, width=5)
        po_entry.grid(row=1, column=2)
        po_modify = tk.Button(prog_frame, text='mod', command=lambda: modify(po_entry, po_pro, 'mee', 'po'))
        po_modify.grid(row=1, column=3, padx=10)

        ta_label = tk.Label(prog_frame, text='Tangents', font=FONT_2)
        ta_label.grid(row=2, column=0)
        ta_pro = tk.Progressbar(prog_frame, value=settings['mee']['ta'], length=200, maximum=100)
        ta_pro.grid(row=2, column=1, padx=10)
        ta_entry = tk.Entry(prog_frame, width=5)
        ta_entry.grid(row=2, column=2)
        ta_modify = tk.Button(prog_frame, text='mod', command=lambda: modify(ta_entry, ta_pro, 'mee', 'ta'))
        ta_modify.grid(row=2, column=3, padx=10)

        lo_label = tk.Label(prog_frame, text='LOCI', font=FONT_2)
        lo_label.grid(row=3, column=0)
        lo_pro = tk.Progressbar(prog_frame, value=settings['mee']['lo'], length=200, maximum=100)
        lo_pro.grid(row=3, column=1, padx=10)
        lo_entry = tk.Entry(prog_frame, width=5)
        lo_entry.grid(row=3, column=2)
        lo_modify = tk.Button(prog_frame, text='mod', command=lambda: modify(lo_entry, lo_pro, 'mee', 'lo'))
        lo_modify.grid(row=3, column=3, padx=10)

        pp_label = tk.Label(prog_frame, text='Pictorial .P', font=FONT_2)
        pp_label.grid(row=4, column=0)
        pp_pro = tk.Progressbar(prog_frame, value=settings['mee']['pp'], length=200, maximum=100)
        pp_pro.grid(row=4, column=1, padx=10)
        pp_entry = tk.Entry(prog_frame, width=5)
        pp_entry.grid(row=4, column=2)
        pp_modify = tk.Button(prog_frame, text='mod', command=lambda: modify(pp_entry, pp_pro, 'mee', 'pp'))
        pp_modify.grid(row=4, column=3, padx=10)

        op_label = tk.Label(prog_frame, text='Orth. Pro', font=FONT_2)
        op_label.grid(row=5, column=0)
        op_pro = tk.Progressbar(prog_frame, value=settings['mee']['op'], length=200, maximum=100)
        op_pro.grid(row=5, column=1, padx=10)
        op_entry = tk.Entry(prog_frame, width=5)
        op_entry.grid(row=5, column=2)
        op_modify = tk.Button(prog_frame, text='mod', command=lambda: modify(op_entry, op_pro, 'mee', 'op'))
        op_modify.grid(row=5, column=3, padx=10)

        fs_label = tk.Label(prog_frame, text='Freehand .S', font=FONT_2)
        fs_label.grid(row=6, column=0)
        fs_pro = tk.Progressbar(prog_frame, value=settings['mee']['fs'], length=200, maximum=100)
        fs_pro.grid(row=6, column=1, padx=10)
        fs_entry = tk.Entry(prog_frame, width=5)
        fs_entry.grid(row=6, column=2)
        fs_modify = tk.Button(prog_frame, text='mod', command=lambda: modify(fs_entry, fs_pro, 'mee', 'fs'))
        fs_modify.grid(row=6, column=3, padx=10)

        main_button = tk.Button(main_frame, text='Main Page', command=lambda: controller.show_frame('MainPage'))
        main_button.pack(pady=10)


class BIO(tk.Frame):
    def __init__(self, parent, controller):
        # MainPage(self, controller=self).destroy()
        tk.Frame.__init__(self, parent, width=675, height=500)
        self.controller = controller

        main_frame = tk.Frame(self, width=700, height=500)
        main_frame.place(x=0, y=0, relx=0, rely=0)
        
        label = tk.Label(main_frame, text='BIO 101 Progress Page', font=FONT_1)
        label.pack(side=tk.TOP, fill=tk.X, pady=10, anchor=tk.CENTER)

        bio_progress = tk.Progressbar(main_frame, value=settings['bio-progress'], maximum=100, length=450)
        bio_progress.pack()

 
        prog_frame = tk.Frame(main_frame)
        prog_frame.pack()

        bi_label = tk.Label(prog_frame, text='Biodi. Clas', font=FONT_2)
        bi_label.grid(row=0, column=0)
        bi_pro = tk.Progressbar(prog_frame, value=settings['bio']['bi'], length=200, maximum=100)
        bi_pro.grid(row=0, column=1, padx=10)
        bi_entry = tk.Entry(prog_frame, width=5)
        bi_entry.grid(row=0, column=2)
        bi_modify = tk.Button(prog_frame, text='mod', command=lambda: modify(bi_entry, bi_pro, 'bio', 'bi'))
        bi_modify.grid(row=0, column=3, padx=10)

        ec_label = tk.Label(prog_frame, text='Eco .Int', font=FONT_2)
        ec_label.grid(row=1, column=0)
        ec_pro = tk.Progressbar(prog_frame, value=settings['bio']['ec'], length=200, maximum=100)
        ec_pro.grid(row=1, column=1, padx=10)
        ec_entry = tk.Entry(prog_frame, width=5)
        ec_entry.grid(row=1, column=2)
        ec_modify = tk.Button(prog_frame, text='mod', command=lambda: modify(ec_entry, ec_pro, 'bio', 'ec'))
        ec_modify.grid(row=1, column=3, padx=10)

        ce_label = tk.Label(prog_frame, text='Cell .Th', font=FONT_2)
        ce_label.grid(row=2, column=0)
        ce_pro = tk.Progressbar(prog_frame, value=settings['bio']['ce'], length=200, maximum=100)
        ce_pro.grid(row=2, column=1, padx=10)
        ce_entry = tk.Entry(prog_frame, width=5)
        ce_entry.grid(row=2, column=2)
        ce_modify = tk.Button(prog_frame, text='mod', command=lambda: modify(ce_entry, ce_pro, 'bio', 'ce'))
        ce_modify.grid(row=2, column=3, padx=10)

        re_label = tk.Label(prog_frame, text='Reproduction', font=FONT_2)
        re_label.grid(row=3, column=0)
        re_pro = tk.Progressbar(prog_frame, value=settings['bio']['re'], length=200, maximum=100)
        re_pro.grid(row=3, column=1, padx=10)
        re_entry = tk.Entry(prog_frame, width=5)
        re_entry.grid(row=3, column=2)
        re_modify = tk.Button(prog_frame, text='mod', command=lambda: modify(re_entry, re_pro, 'bio', 're'))
        re_modify.grid(row=3, column=3, padx=10)

        va_label = tk.Label(prog_frame, text='Variations', font=FONT_2)
        va_label.grid(row=4, column=0)
        va_pro = tk.Progressbar(prog_frame, value=settings['bio']['va'], length=200, maximum=100)
        va_pro.grid(row=4, column=1, padx=10)
        va_entry = tk.Entry(prog_frame, width=5)
        va_entry.grid(row=4, column=2)
        va_modify = tk.Button(prog_frame, text='mod', command=lambda: modify(va_entry, va_pro, 'bio', 'va'))
        va_modify.grid(row=4, column=3, padx=10)

        bp_label = tk.Label(prog_frame, text='Bro .pte', font=FONT_2)
        bp_label.grid(row=5, column=0)
        bp_pro = tk.Progressbar(prog_frame, value=settings['bio']['bp'], length=200, maximum=100)
        bp_pro.grid(row=5, column=1, padx=10)
        bp_entry = tk.Entry(prog_frame, width=5)
        bp_entry.grid(row=5, column=2)
        bp_modify = tk.Button(prog_frame, text='mod', command=lambda: modify(bp_entry, bp_pro, 'bio', 'bp'))
        bp_modify.grid(row=5, column=3, padx=10)

        af_label = tk.Label(prog_frame, text='Angio .FlowP', font=FONT_2)
        af_label.grid(row=6, column=0)
        af_pro = tk.Progressbar(prog_frame, value=settings['bio']['af'], length=200, maximum=100)
        af_pro.grid(row=6, column=1, padx=10)
        af_entry = tk.Entry(prog_frame, width=5)
        af_entry.grid(row=6, column=2)
        af_modify = tk.Button(prog_frame, text='mod', command=lambda: modify(af_entry, af_pro, 'bio', 'af'))
        af_modify.grid(row=6, column=3, padx=10)

        vf_label = tk.Label(prog_frame, text='Virus. F...', font=FONT_2)
        vf_label.grid(row=7, column=0)
        vf_pro = tk.Progressbar(prog_frame, value=settings['bio']['vf'], length=200, maximum=100)
        vf_pro.grid(row=7, column=1, padx=10)
        vf_entry = tk.Entry(prog_frame, width=5)
        vf_entry.grid(row=7, column=2)
        vf_modify = tk.Button(prog_frame, text='mod', command=lambda: modify(vf_entry, vf_pro, 'bio', 'vf'))
        vf_modify.grid(row=7, column=3, padx=10)

        main_button = tk.Button(main_frame, text='Main Page', command=lambda: controller.show_frame('MainPage'))
        main_button.pack(pady=10)


class GNS1(tk.Frame):
    def __init__(self, parent, controller):
        # MainPage(self, controller=self).destroy()
        tk.Frame.__init__(self, parent, width=675, height=500)
        self.controller = controller

        main_frame = tk.Frame(self, width=700, height=500)
        main_frame.place(x=0, y=0, relx=0, rely=0)
        
        label = tk.Label(main_frame, text='GNS 101 Progress Page', font=FONT_1)
        label.pack(side=tk.TOP, fill=tk.X, pady=10, anchor=tk.CENTER)

        gns101_progress = tk.Progressbar(main_frame, value=settings['gns1-progress'], maximum=100, length=450)
        gns101_progress.pack()

 
        prog_frame = tk.Frame(main_frame)
        prog_frame.pack()

        tm_label = tk.Label(prog_frame, text='Time .GS', font=FONT_2)
        tm_label.grid(row=0, column=0)
        tm_pro = tk.Progressbar(prog_frame, value=settings['gns1']['tm'], length=200, maximum=100)
        tm_pro.grid(row=0, column=1, padx=10)
        tm_entry = tk.Entry(prog_frame, width=5)
        tm_entry.grid(row=0, column=2)
        tm_modify = tk.Button(prog_frame, text='mod', command=lambda: modify(tm_entry, tm_pro, 'gns1', 'tm'))
        tm_modify.grid(row=0, column=3, padx=10)

        ss_label = tk.Label(prog_frame, text='Study Skills', font=FONT_2)
        ss_label.grid(row=1, column=0)
        ss_pro = tk.Progressbar(prog_frame, value=settings['gns1']['ss'], length=200, maximum=100)
        ss_pro.grid(row=1, column=1, padx=10)
        ss_entry = tk.Entry(prog_frame, width=5)
        ss_entry.grid(row=1, column=2)
        ss_modify = tk.Button(prog_frame, text='mod', command=lambda: modify(ss_entry, ss_pro, 'gns1', 'ss'))
        ss_modify.grid(row=1, column=3, padx=10)

        wf_label = tk.Label(prog_frame, text='Word .For', font=FONT_2)
        wf_label.grid(row=2, column=0)
        wf_pro = tk.Progressbar(prog_frame, value=settings['gns1']['wf'], length=200, maximum=100)
        wf_pro.grid(row=2, column=1, padx=10)
        wf_entry = tk.Entry(prog_frame, width=5)
        wf_entry.grid(row=2, column=2)
        wf_modify = tk.Button(prog_frame, text='mod', command=lambda: modify(wf_entry, wf_pro, 'gns1', 'wf'))
        wf_modify.grid(row=2, column=3, padx=10)

        ps_label = tk.Label(prog_frame, text='Part os Speech', font=FONT_2)
        ps_label.grid(row=3, column=0)
        ps_pro = tk.Progressbar(prog_frame, value=settings['gns1']['ps'], length=200, maximum=100)
        ps_pro.grid(row=3, column=1, padx=10)
        ps_entry = tk.Entry(prog_frame, width=5)
        ps_entry.grid(row=3, column=2)
        ps_modify = tk.Button(prog_frame, text='mod', command=lambda: modify(ps_entry, ps_pro, 'gns1', 'ps'))
        ps_modify.grid(row=3, column=3, padx=10)

        nt_label = tk.Label(prog_frame, text='Note .Tak', font=FONT_2)
        nt_label.grid(row=4, column=0)
        nt_pro = tk.Progressbar(prog_frame, value=settings['gns1']['nt'], length=200, maximum=100)
        nt_pro.grid(row=4, column=1, padx=10)
        nt_entry = tk.Entry(prog_frame, width=5)
        nt_entry.grid(row=4, column=2)
        nt_modify = tk.Button(prog_frame, text='mod', command=lambda: modify(nt_entry, nt_pro, 'gns1', 'nt'))
        nt_modify.grid(row=4, column=3, padx=10)

        main_button = tk.Button(main_frame, text='Main Page', command=lambda: controller.show_frame('MainPage'))
        main_button.pack(pady=10)


class GNS3(tk.Frame):
    def __init__(self, parent, controller):
        # MainPage(self, controller=self).destroy()
        tk.Frame.__init__(self, parent, width=675, height=500)
        self.controller = controller

        main_frame = tk.Frame(self, width=700, height=500)
        main_frame.place(x=0, y=0, relx=0, rely=0)
        
        label = tk.Label(main_frame, text='GNS 101 Progress Page', font=FONT_1)
        label.pack(side=tk.TOP, fill=tk.X, pady=10, anchor=tk.CENTER)

        gns103_progress = tk.Progressbar(main_frame, value=settings['gns3-progress'], maximum=100, length=450)
        gns103_progress.pack()

 
        prog_frame = tk.Frame(main_frame)
        prog_frame.pack()

        c12_label = tk.Label(prog_frame, text='Ch 1 & 2', font=FONT_2)
        c12_label.grid(row=0, column=0)
        c12_pro = tk.Progressbar(prog_frame, value=settings['gns3']['c12'], length=200, maximum=100)
        c12_pro.grid(row=0, column=1, padx=10)
        c12_entry = tk.Entry(prog_frame, width=5)
        c12_entry.grid(row=0, column=2)
        c12_modify = tk.Button(prog_frame, text='mod', command=lambda: modify(c12_entry, c12_pro, 'gns3', 'c12'))
        c12_modify.grid(row=0, column=3, padx=10)

        c34_label = tk.Label(prog_frame, text='Ch 3 & 4', font=FONT_2)
        c34_label.grid(row=1, column=0)
        c34_pro = tk.Progressbar(prog_frame, value=settings['gns3']['c34'], length=200, maximum=100)
        c34_pro.grid(row=1, column=1, padx=10)
        c34_entry = tk.Entry(prog_frame, width=5)
        c34_entry.grid(row=1, column=2)
        c34_modify = tk.Button(prog_frame, text='mod', command=lambda: modify(c34_entry, c34_pro, 'gns3', 'c34'))
        c34_modify.grid(row=1, column=3, padx=10)

        c56_label = tk.Label(prog_frame, text='Ch 5 & 6', font=FONT_2)
        c56_label.grid(row=2, column=0)
        c56_pro = tk.Progressbar(prog_frame, value=settings['gns3']['c56'], length=200, maximum=100)
        c56_pro.grid(row=2, column=1, padx=10)
        c56_entry = tk.Entry(prog_frame, width=5)
        c56_entry.grid(row=2, column=2)
        c56_modify = tk.Button(prog_frame, text='mod', command=lambda: modify(c56_entry, c56_pro, 'gns3', 'c56'))
        c56_modify.grid(row=2, column=3, padx=10)

        c78_label = tk.Label(prog_frame, text='Ch 7 & 8', font=FONT_2)
        c78_label.grid(row=3, column=0)
        c78_pro = tk.Progressbar(prog_frame, value=settings['gns3']['c78'], length=200, maximum=100)
        c78_pro.grid(row=3, column=1, padx=10)
        c78_entry = tk.Entry(prog_frame, width=5)
        c78_entry.grid(row=3, column=2)
        c78_modify = tk.Button(prog_frame, text='mod', command=lambda: modify(c78_entry, c78_pro, 'gns3', 'c78'))
        c78_modify.grid(row=3, column=3, padx=10)

        main_button = tk.Button(main_frame, text='Main Page', command=lambda: controller.show_frame('MainPage'))
        main_button.pack(pady=10)


class CHE(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, width=675, height=500)
        self.controller = controller

        main_frame = tk.Frame(self, width=700, height=500)
        main_frame.place(x=0, y=0, relx=0, rely=0)
        
        label = tk.Label(main_frame, text='PHY 101 Progress Page', font=FONT_1)
        label.pack(side=tk.TOP, fill=tk.X, pady=10, anchor=tk.CENTER)

        che_progress = tk.Progressbar(main_frame, value=settings['che-progress'], maximum=100, length=450)
        che_progress.pack()


 
        prog_frame = tk.Frame(main_frame)
        prog_frame.pack()

        at_label = tk.Label(prog_frame, text='Atomic .Th', font=FONT_2)
        at_label.grid(row=0, column=0)
        at_pro = tk.Progressbar(prog_frame, value=settings['che']['at'], length=200, maximum=100)
        at_pro.grid(row=0, column=1, padx=10)
        at_entry = tk.Entry(prog_frame, width=5)
        at_entry.grid(row=0, column=2)
        at_modify = tk.Button(prog_frame, text='mod', command=lambda: modify(at_entry, at_pro, 'che', 'at'))
        at_modify.grid(row=0, column=3, padx=10)

        ea_label = tk.Label(prog_frame, text='Eletronic .Th', font=FONT_2)
        ea_label.grid(row=1, column=0)
        ea_pro = tk.Progressbar(prog_frame, value=settings['che']['ea'], length=200, maximum=100)
        ea_pro.grid(row=1, column=1, padx=10)
        ea_entry = tk.Entry(prog_frame, width=5)
        ea_entry.grid(row=1, column=2)
        ea_modify = tk.Button(prog_frame, text='mod', command=lambda: modify(ea_entry, ea_pro, 'che', 'ea'))
        ea_modify.grid(row=1, column=3, padx=10)

        ce_label = tk.Label(prog_frame, text='Chemical .Eq', font=FONT_2)
        ce_label.grid(row=2, column=0)
        ce_pro = tk.Progressbar(prog_frame, value=settings['che']['ce'], length=200, maximum=100)
        ce_pro.grid(row=2, column=1, padx=10)
        ce_entry = tk.Entry(prog_frame, width=5)
        ce_entry.grid(row=2, column=2)
        ce_modify = tk.Button(prog_frame, text='mod', command=lambda: modify(ce_entry, ce_pro, 'che', 'ce'))
        ce_modify.grid(row=2, column=3, padx=10)

        ck_label = tk.Label(prog_frame, text='Chemical .K', font=FONT_2)
        ck_label.grid(row=3, column=0)
        ck_pro = tk.Progressbar(prog_frame, value=settings['che']['ck'], length=200, maximum=100)
        ck_pro.grid(row=3, column=1, padx=10)
        ck_entry = tk.Entry(prog_frame, width=5)
        ck_entry.grid(row=3, column=2)
        ck_modify = tk.Button(prog_frame, text='mod', command=lambda: modify(ck_entry, ck_pro, 'che', 'ck'))
        ck_modify.grid(row=3, column=3, padx=10)

        tc_label = tk.Label(prog_frame, text='Thermo .CH', font=FONT_2)
        tc_label.grid(row=4, column=0)
        tc_pro = tk.Progressbar(prog_frame, value=settings['che']['tc'], length=200, maximum=100)
        tc_pro.grid(row=4, column=1, padx=10)
        tc_entry = tk.Entry(prog_frame, width=5)
        tc_entry.grid(row=4, column=2)
        tc_modify = tk.Button(prog_frame, text='mod', command=lambda: modify(tc_entry, tc_pro, 'che', 'tc'))
        tc_modify.grid(row=4, column=3, padx=10)

        ec_label = tk.Label(prog_frame, text='Electro .Ch', font=FONT_2)
        ec_label.grid(row=5, column=0)
        ec_pro = tk.Progressbar(prog_frame, value=settings['che']['ec'], length=200, maximum=100)
        ec_pro.grid(row=5, column=1, padx=10)
        ec_entry = tk.Entry(prog_frame, width=5)
        ec_entry.grid(row=5, column=2)
        ec_modify = tk.Button(prog_frame, text='mod', command=lambda: modify(ec_entry, ec_pro, 'che', 'ec'))
        ec_modify.grid(row=5, column=3, padx=10)

        ra_label = tk.Label(prog_frame, text='Radio .A', font=FONT_2)
        ra_label.grid(row=6, column=0)
        ra_pro = tk.Progressbar(prog_frame, value=settings['che']['ra'], length=200, maximum=100)
        ra_pro.grid(row=6, column=1, padx=10)
        ra_entry = tk.Entry(prog_frame, width=5)
        ra_entry.grid(row=6, column=2)
        ra_modify = tk.Button(prog_frame, text='mod', command=lambda: modify(ra_entry, ra_pro, 'che', 'ra'))
        ra_modify.grid(row=6, column=3, padx=10)

        sl_label = tk.Label(prog_frame, text='Solution', font=FONT_2)
        sl_label.grid(row=7, column=0)
        sl_pro = tk.Progressbar(prog_frame, value=settings['che']['sl'], length=200, maximum=100)
        sl_pro.grid(row=7, column=1, padx=10)
        sl_entry = tk.Entry(prog_frame, width=5)
        sl_entry.grid(row=7, column=2)
        sl_modify = tk.Button(prog_frame, text='mod', command=lambda: modify(sl_entry, sl_pro, 'che', 'sl'))
        sl_modify.grid(row=7, column=3, padx=10)

        main_button = tk.Button(main_frame, text='Main Page', command=lambda: controller.show_frame('MainPage'))
        main_button.pack(pady=10)



if __name__ == "__main__":
    app = App()
    print(diff)
    print(days_left)
    app.mainloop()


