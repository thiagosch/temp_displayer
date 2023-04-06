import json
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
moreno = open(f'moreno_final.json')
moreno = json.load(moreno)

escobar = open(f'escobar_final.json')
escobar = json.load(escobar)

laplata = open(f'laplata_final.json')
laplata = json.load(laplata)

sanpedro = open(f'sanPedro_final.json')
sanpedro = json.load(sanpedro)



def generate_tables(data,city):
# convert the data to a pandas DataFrame
    df = pd.DataFrame.from_dict(data, orient='index')
    df = df.round(2)
    df_styled = df.style.format({
        'hum': '{:.1f}%',
        'max': '{:.0f}C',
        'min': '{:.1f}C',
        'avg': '{:.1f}C',
        'prec': '{:.1f}mm'
    })
    df_styled = df_styled.set_caption(city)
    # Print the dataframe
    # Open the file in append mode and write the new data
    with open('test.html', 'a') as f:
        f.write(df_styled.to_html())

    print(df_styled.to_html())


generate_tables(laplata,'La Plata')
generate_tables(moreno, 'Moreno')
generate_tables(escobar, 'Escobar')
generate_tables(sanpedro, 'San Pedro')