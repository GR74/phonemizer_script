# -*- coding: utf-8 -*-
def plot_normalized_gamma_across_channels(EEG_Welch_Spectra, ElectrodeList, Trials):
    """
    

    Parameters
    ----------
    EEG_Welch_Spectra : Dict of Lists
        Output from EEG_Implement_Welch and contains all welch transform data from the EEG
    ElectrodeList : List
        All electrodes that took data, this is the same value input as in EEG_Implement_Welch
    Trials : Int
        Number of trials in the raw EEG dataset. This value is a return of EEG_Implement_Welch

    Returns
    -------
    WelchPoints : Dict of Lists
        The final dictionary of all CMRO2 data per 0.25 seconds via the raw EEG data.

    """
    
    
    """Plots globally normalized Gamma band power (0 to 1) over time for all electrodes on one graph."""
    import numpy as np
    import math
    from scipy.signal import welch
    
    time_axis = [i * 0.25 for i in range(8)]  # 0.25s per segment
    all_gamma_values = []

    # Collect all gamma values from all electrodes
    for electrode in ElectrodeList:
        trial_key = f'{electrode} trial '+ str(Trials)
        if trial_key in EEG_Welch_Spectra:
            gamma_power = [
                seg['band_power']['Gamma'] for seg in EEG_Welch_Spectra[trial_key]['segments']
            ]
            all_gamma_values.extend(gamma_power)

    # Compute global min and max
    global_min = min(all_gamma_values)
    global_max = max(all_gamma_values)
    
    #Dictionary setup for all CMRO2 values based on the normalized gamma value
    WelchPoints = {}
    for TrialsKeep in range(Trials):
        for electrode in ElectrodeList:
            trial_key = f'{electrode} trial '+ str(TrialsKeep)
            if trial_key not in EEG_Welch_Spectra:
                continue
            
            #Separating out gamma values into a list coordinated to the electrodes
            gamma_power = [
                seg['band_power']['Gamma'] for seg in EEG_Welch_Spectra[trial_key]['segments']
            ]
    
            # Normalize using global min and max
            if global_max - global_min == 0:
                normalized = [0.0 for _ in gamma_power]  # Avoid division by zero
            else:
                #Final valuation toward CMRO2, "normalized" is used as CMRO2 to be plugged into the neurovascular variables
                #we had an estimated max ~3.02 and a resting at ~2.10. This addition result gave best range considering we normalized about 0.0-1.0
                #If changes were to be made to improve correlative viability, finding better CMRO2 resting and maximum values would be implemented here
                normalized = [2.1+((val - global_min) / (global_max - global_min)) for val in gamma_power]
    
            WelchPoints[trial_key] = normalized
        
    return WelchPoints
        
