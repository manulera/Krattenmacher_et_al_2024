#%%
import glob

folders = glob.glob('./run*/')
folders.sort()
complete_html = ''
for folder in folders:
    folder_html = f'<h1>{folder}</h1>'
    imas = glob.glob(f'./{folder}/plots/*.svg')
    imas.sort()
    
    # Separate fits and data plots
    data_figures = list()
    fitness_figures = list()
    for ima in imas:
        if 'fitness' in ima:
            fitness_figures.append(ima)
        else:
            data_figures.append(ima)
    
    # folder_html+='<h2>Data</h2>'
    # for ima in data_figures:
    #     folder_html+= f'<img src="./{ima}" width="300">'

    folder_html+='<h2>Fitness</h2>'
    for ima in fitness_figures:
        folder_html+= f'<img src="./{ima}" width="300">'

    folder_html+='<h2>Main</h2>'
    for svg in ['shrinking_speed_steady_state.svg','accumulation_timescale.svg','accumulation_end_fit.svg']:
        ima = f'./{folder}/plots/{svg}'
        folder_html+= f'<img src="./{ima}" width="300">'

    complete_html+=folder_html

# Read in the file
with open('template.html', 'r') as file :
  temp = file.read()

# Write the file out again
with open('see_plots.html', 'w') as file:
  file.write(temp.replace('subs', complete_html))