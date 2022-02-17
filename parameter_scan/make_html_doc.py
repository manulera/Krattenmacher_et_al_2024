#%%
import glob

folders = glob.glob('./run*/')
folders.sort()
complete_html = ''
for folder in folders:
    folder_html = f'<h1>{folder}</h1>'
    imas = glob.glob(f'./{folder}/plots/*.svg')
    imas.sort()
    for ima in imas:
        folder_html+= f'<img src="./{ima}" width="300">'
    complete_html+=folder_html

# Read in the file
with open('template.html', 'r') as file :
  temp = file.read()

# Write the file out again
with open('see_plots.html', 'w') as file:
  file.write(temp.replace('subs', complete_html))