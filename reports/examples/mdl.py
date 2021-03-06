import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from reports import mdl_results
from rolldecayestimators import logarithmic_decrement
from rolldecayestimators import lambdas
from sklearn.pipeline import Pipeline
from rolldecayestimators import measure
from rolldecayestimators.direct_estimator_cubic import EstimatorQuadraticB, EstimatorCubic, EstimatorQuadratic

def get_models_zero_speed():
    mask = mdl_results.df_rolldecays['ship_speed'] == 0
    df_rolldecays_zero = mdl_results.df_rolldecays.loc[mask].copy()
    return _get_models(df=df_rolldecays_zero)

def get_models_speed():
    mask = mdl_results.df_rolldecays['ship_speed'] > 0
    df_rolldecays = mdl_results.df_rolldecays.loc[mask].copy()
    return _get_models(df=df_rolldecays)

def get_models():
    df = mdl_results.df_rolldecays
    return _get_models(df=df)

def _get_models(df):
        
    models = {}
    for id, row in df.iterrows():
        model_file_path = '../../models/KVLCC2_%i.pkl' % id
        
        models[id] = joblib.load(model_file_path)['estimator'] 

    return models

def gather_results(models):
    
    df_results = pd.DataFrame()
    for id, model in models.items():

        row = mdl_results.df_rolldecays.loc[id]
        scale_factor = row.scale_factor
        meta_data = {
            'Volume' : row.Volume/(scale_factor**3),
            'rho' : row.rho,
            'g' : row.g,
            'GM' : row.gm/scale_factor,
            }

        results = model.result_for_database(meta_data=meta_data)
        results = pd.Series(results, name=id)
        results['paper_name'] = row.paper_name
        results['id'] = row.name
        df_results = df_results.append(results)
    df_results = df_results.astype(float)
    df_results['id'] = df_results['id'].astype(int)
    df_results['paper_name'] = df_results['paper_name'].astype(int)
    df_results['method'] = 'model test'

    return df_results

def analyze_amplitudes(models):
    amplitudes = {}
    for id,model in models.items():
        
        AttributeError
        try:
            df_amplitudes = analyze_amplitude(model=model)
        except AttributeError:
            raise ValueError(id)
        
        amplitudes[id] = df_amplitudes

    return amplitudes

def analyze_amplitude(model):
    
    #df_max = logarithmic_decrement.find_peaks(model.X)
    df_max = measure.get_peaks(model.X)
    df_max_model = measure.get_peaks(model.predict(model.X))
    
    results = model.results
    ## Logartithmic decrement
    df_amplitudes = df_max.copy()
    df_amplitudes_model = df_max_model.copy()
    
    df_decrements = logarithmic_decrement.calculate_decrements(df_amplitudes=df_amplitudes)
    df_amplitudes['zeta_n'] = logarithmic_decrement.calculate_zeta(df_decrements=df_decrements)
    df_amplitudes['B'] = logarithmic_decrement.calculate_B(zeta_n=df_amplitudes['zeta_n'], 
                                                           A_44=results['A_44'], omega0=results['omega0'])
    df_amplitudes['phi_a'] = logarithmic_decrement.estimate_amplitude(phi=df_amplitudes['phi'])
    
    omega0 = results['omega0']
    
    if type(model) is EstimatorCubic:    
        df_amplitudes['B_model'] = lambdas.B_e_lambda_cubic(B_1=results['B_1'], B_2=results['B_2'], 
                                                    B_3=results['B_3'],
                            omega0=omega0, phi_a=df_amplitudes['phi_a'])
    
    elif (type(model) is EstimatorQuadraticB) or (type(model) is EstimatorQuadratic):
        df_amplitudes['B_model'] = lambdas.B_e_lambda(B_1=results['B_1'], B_2=results['B_2'], 
                            omega0=omega0, phi_a=df_amplitudes['phi_a'])

    else:
        raise ValueError('Unknown model class:%s' % model.__class__)
    
    df_amplitudes['B_model'] = df_amplitudes['B_model'].astype(float)
    
    
    t = np.array(df_amplitudes.index)
    df_amplitudes['T'] = np.roll(t,-2) - t
    df_amplitudes['omega0'] = 2*np.pi/df_amplitudes['T']
    
    t = np.array(df_amplitudes_model.index)
    df_amplitudes_model['T'] = np.roll(t,-2) - t
    df_amplitudes_model['omega0'] = 2*np.pi/df_amplitudes_model['T']
    df_amplitudes['omega0_model'] = np.array(df_amplitudes_model['omega0'].astype(float))

    df_amplitudes.dropna(inplace=True, subset=['B'])

    return df_amplitudes

def plot_amplitudes(df_amplitudes, paper_name, source='model test', prefix='B', ax=None, model=True, **kwargs):
    
    if ax is None:
        fig,ax=plt.subplots()
    
    df_amplitudes.sort_values(by='phi_a', inplace=True)
    
    pretty = r'$\phi_a$'
    df_amplitudes[pretty] = np.rad2deg(df_amplitudes['phi_a'])
    
    label='Run %i: %s' % (paper_name, source)
    
    df_amplitudes.plot(x=pretty, y=prefix, label=label, style='.', alpha=0.5, ax=ax, **kwargs)
    color=ax.get_lines()[-1].get_color()
    
    label='Run %i: model' % paper_name
    df_amplitudes.plot(x=pretty, y='%s_model' % prefix, label='_nolegend_', color=color, style='-', ax=ax)
    ax.grid(True)

def show(amplitudes, df_results, ylim=None, source='model test'):
    
    ## Plotting:
    prefixes = ['B','omega0']
    ylabels = [r'$B$ $[Nm \cdot s]$',
               r'$\omega_0$ $[\frac{rad}{s}]$',
    ]
    
    fig,axes=plt.subplots(nrows=len(prefixes))

    for ax, prefix, ylabel in zip(axes,prefixes, ylabels):
        
        for id,row in df_results.iterrows(): 
            df_amplitudes = amplitudes[id].copy()
            plot_amplitudes(df_amplitudes=df_amplitudes, paper_name = row.paper_name, ax=ax, source=source, prefix=prefix)

        ax.set_ylabel(ylabel)    
        ax.set_xlabel(r'$\phi_a$ $[deg]$')
        ax.grid(True)
    
    ax = axes[0]
    ax.get_legend().set_visible(False)
    #ax.get_xaxis().set_visible(False)
    ax.set_xlabel('')
    ax.set_ylim(ylim)
    ax.grid(True)
    ax.set_yticks(np.arange(2,ylim[1],2))
    #ax.set_xticks([])
    ax.set_xticklabels([])
    
    ax = axes[1]
    ax.legend(loc='lower right')
        
    