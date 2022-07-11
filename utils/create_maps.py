"""
Author: Neel Dhulipala
Project: Air Partners

Script to create maps for every sensor.
"""

import os
import pandas as pd
import plotly.graph_objects as go

def _read_token(token_path):
        with open(token_path, 'r') as f:
            token = f.read()
            return token

MAPBOX_TOKEN = _read_token('mapbox_token.txt')

def get_lats_and_longs(sn_list, sn_dict):
    for i in range(len(sn_list) -1,-1,-1):
        sn = sn_list[i]
        if sn_dict[sn].shape == (0,0):
            sn_list.pop(i)   
    sn_locs = pd.DataFrame()
    sn_locs['sensor'] = sn_list
    sn_locs['lats'] = [sn_dict[sn].iloc[-1]['geo']['lat'] for sn in sn_list]
    sn_locs['longs'] = [sn_dict[sn].iloc[-1]['geo']['lon'] for sn in sn_list]
    sn_locs = sn_locs.set_index('sensor')
    return sn_locs

def show(df, sn_list):
    data = go.Scattermapbox(lat=list(df['lats']),
                            lon=list(df['longs']),
                            mode='markers+text',
                            marker=dict(size=30, color='green'),
                            textposition='top center',
                            textfont=dict(size=28, color='black'),
                            text=[sn_list[i] for i in range(len(sn_list))])
    
    # Create folder for images if does not already exist
    if not os.path.exists('_images/locs'):
        os.mkdir('_images/locs')
    # Iterate through all sensors and create images for each one
    for sn in sn_list:
        # Layout graphic so that image centers on sensor in question
        layout = dict(margin=dict(l=0, t=0, r=0, b=0, pad=0),
                mapbox=dict(accesstoken=MAPBOX_TOKEN,
                            center=dict(lat=df['lats'][sn], lon=df['longs'][sn]),
                            style='basic',
                            zoom=14))
        fig = go.Figure(data=data, layout=layout)
        
        
        # creates image twice in case figure not fully complete by first iteration
        fig.write_image(f'_images/locs/{sn}.png', format='png', engine="kaleido")
        fig.write_image(f'_images/locs/{sn}.png')
        print(f'Finished {sn} image.')

def main(sn_list, sn_dict):
    df = get_lats_and_longs(sn_list, sn_dict)
    show(df, sn_list)