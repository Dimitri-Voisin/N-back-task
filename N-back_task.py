
#
# Author Dimitri Voisin (Phd Student CRCN-UR2NF / LN2T) 
# up to date 10/26
# This script exectue a N-back task depending on parameter you give (N = X; number of trials; number of target)

# Sorry comments are in French and English its how my brain works :)

# Import library
import os
import sys
import random
from psychopy import visual, core, gui, data, event
from psychopy.hardware import keyboard


# Setup experiment and parameters
def setup_experiment():
    """Affiche la boîte de dialogue et génère un nom de fichier au format BIDS."""
    exp_info = {
        'Participant': '',
        'Session': '',
        'Condition': '',
        'N-back': 2,
        'Nombre essais': 50,
        '% cibles (0-100)': 30
    }
    
    dlg = gui.DlgFromDict(dictionary=exp_info, sortKeys=False, title='Tâche N-Back')
    if not dlg.OK:
        core.quit()
        
    date_str = data.getDateStr(format="%Y%m%d_%H%M")
    exp_info['date'] = date_str
    
    # Nom de fichier BIDS
    bids_filename = (f"sub-{exp_info['Participant']}_"
                     f"ses-{exp_info['Session']}_"
                     f"task-{exp_info['N-back']}back_"
                     f"cond-{exp_info['Condition']}_"
                     f"trials-{exp_info['Nombre essais']}_"
                     f"tgt-{exp_info['% cibles (0-100)']}_"
                     f"date-{date_str}")
                     
    os.makedirs('data', exist_ok=True)
    filename = f"data/{bids_filename}"
    
    exp_data = data.ExperimentHandler(name=f"{exp_info['N-back']}back", version='1.0',
                                      extraInfo=exp_info, dataFileName=filename)
                                      
    return exp_data, exp_info

def generate_nback_sequence(n_trials, target_percent, n_back):
    """Génère une séquence modulable selon le paramètre N-back choisi."""
    digits = list(range(1, 10))
    seq = []
    is_target = []
    
    # 1. Amorçage : Les N premiers essais (ne peuvent pas être des cibles)
    for _ in range(n_back):
        seq.append(random.choice(digits))
        is_target.append(0)
    
    # 2. Calcul du nombre exact de cibles
    n_targets = int(round(n_trials * (target_percent / 100.0)))
    
    # Les cibles ne peuvent apparaître qu'à partir de l'essai N
    available_slots = list(range(n_back, n_trials))
    
    # Sécurité si on demande plus de cibles que de slots disponibles
    if n_targets > len(available_slots):
        n_targets = len(available_slots)
        
    target_positions = set(random.sample(available_slots, n_targets))
    
    # 3. Remplissage de la séquence
    for i in range(n_back, n_trials):
        if i in target_positions:
            # Cible N-back
            seq.append(seq[i - n_back])
            is_target.append(1)
        else:
            # Non-cible (différent du N-back)
            available = [d for d in digits if d != seq[i - n_back]]
            seq.append(random.choice(available))
            is_target.append(0)
            
    return seq, is_target

def run_block(win, exp_data, kb, seq, is_target, phase="test"):
    """Exécute les essais et enregistre la phase (practice ou test)."""
    fixation = visual.TextStim(win, text='+', height=0.05, color='white')
    digit_stim = visual.TextStim(win, text='', height=0.15, color='white')
    
    fixation_dur = 0.5
    stim_dur = 1.0
    iti_dur = 0.5
    
    for i in range(len(seq)):
        digit_stim.text = str(seq[i])
        
        # Phase 1: Fixation
        fixation.draw()
        win.flip()
        core.wait(fixation_dur)
        
        # Phase 2: Stimulus
        kb.clock.reset()
        kb.clearEvents()
        
        digit_stim.draw()
        win.flip()
        
        keys = kb.waitKeys(maxWait=stim_dur, keyList=['space', 'escape'], waitRelease=False)
        
        # Phase 3: ITI
        win.flip()
        core.wait(iti_dur)
        
        # Traitement de la réponse
        response = 0
        rt = None
        if keys:
            if 'escape' in [k.name for k in keys]:
                win.close()
                core.quit()
            response = 1
            rt = keys[0].rt
            
        correct = 1 if response == is_target[i] else 0
        
        # Sauvegarde
        exp_data.addData('phase', phase)
        exp_data.addData('trial', i+1)
        exp_data.addData('stimulus', seq[i])
        exp_data.addData('is_target', is_target[i])
        exp_data.addData('response', response)
        exp_data.addData('rt', rt)
        exp_data.addData('correct', correct)
        exp_data.nextEntry()

def main():
    exp_data, exp_info = setup_experiment()
    win = visual.Window(fullscr=True, color='black', units='height', allowGUI=False)
    kb = keyboard.Keyboard()
    
    n_trials = int(exp_info['Nombre essais'])
    target_percent = float(exp_info['% cibles (0-100)'])
    n_back = int(exp_info['N-back'])
    
    # --- CONSIGNES DYNAMIQUES ---
    if n_back == 1:
        instruction_text = "Appuyez sur ESPACE si le chiffre correspond\nà celui présenté juste avant (1 essai avant)."
    else:
        instruction_text = f"Appuyez sur ESPACE si le chiffre correspond\nà celui présenté {n_back} essais avant."
        
    instructions = visual.TextStim(win, text=instruction_text + "\n\nNous allons commencer par un court entraînement.\n\nAppuyez sur ESPACE pour commencer.",
                                   height=0.05, color='white')
    instructions.draw()
    win.flip()
    kb.clearEvents()
    kb.waitKeys(keyList=['space'])
    
    # --- PHASE D'ENTRAÎNEMENT (10 essais) ---
    seq_prac, tgt_prac = generate_nback_sequence(n_trials=10, target_percent=30, n_back=n_back)
    run_block(win, exp_data, kb, seq_prac, tgt_prac, phase="practice")
    
    # --- TRANSITION ---
    transition = visual.TextStim(win, text="L'entraînement est terminé.\nNous allons maintenant passer à la tâche principale.\n\nAppuyez sur ESPACE pour démarrer.",
                                 height=0.05, color='white')
    transition.draw()
    win.flip()
    kb.clearEvents()
    kb.waitKeys(keyList=['space'])
    
    # --- TÂCHE PRINCIPALE ---
    seq_main, tgt_main = generate_nback_sequence(n_trials, target_percent, n_back)
    run_block(win, exp_data, kb, seq_main, tgt_main, phase="test")
    
    # --- FIN ---
    end_msg = visual.TextStim(win, text="Fin de l'expérience. Merci !", height=0.05, color='white')
    end_msg.draw()
    win.flip()
    core.wait(2.0)
    
    win.close()
    core.quit()

if __name__ == '__main__':
    main()