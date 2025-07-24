import time
import os
from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import CheckpointCallback
from src.ia.CardGameEnv import CardGameEnv
import numpy as np

def train_model(total_timesteps=500_000, save_path="ppo_cardgame", resume=True):
    env = CardGameEnv()
    
    # Callback pour enregistrer le modèle périodiquement
    checkpoint_callback = CheckpointCallback(
        save_freq=10_000,
        save_path='./models/',
        name_prefix='ppo_cardgame'
    )
    
    model_path = save_path + ".zip"

    if resume and os.path.exists(model_path):
        print(f"[INFO] Chargement du modèle existant depuis {model_path}...")
        model = PPO.load(model_path, env=env)
    else:
        print("[INFO] Nouveau modèle PPO créé.")
        model = PPO("MlpPolicy", env, verbose=1)
    
    print("[TRAINING] Entraînement du modèle...")
    model.learn(total_timesteps=total_timesteps, callback=checkpoint_callback)

    # Sauvegarde finale
    model.save(save_path)
    print(f"[TRAINING] Modèle sauvegardé dans {save_path}.\n")

def test_model(load_path="ppo_cardgame"):
    env = CardGameEnv(verbose=True)

    print(f"[TEST] Chargement du modèle depuis {load_path}...")
    model = PPO.load(load_path, env=env)

    obs = env.reset()

    done = False
    step = 0

    print("[TEST] Début du test de l'agent :\n")
    while not done:
        action, _states = model.predict(obs)
        print(f"Step {step} | Observation: {obs}")
        print(f"Step {step} | Action: {action}")
        obs, reward, done, info = env.step(action)
        print(f"Step {step} | Reward: {reward}, Done: {done}")
        print(f"Step {step} | obs: {obs}\n")
        step += 1


test_model()