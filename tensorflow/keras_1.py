from tensorflow.keras import Input, Model
from tensorflow.keras.layers import Dense, Concatenate
# Définition des inputs
input_a = Input(shape=(32,), name='input_a')
input_b = Input(shape=(64,), name='input_b')
# Branches séparées
branch_a = Dense(64, activation='relu')(input_a)
branch_b = Dense(64, activation='relu')(input_b)
# Fusion des branches
merged = Concatenate()([branch_a, branch_b])
# Couches communes
output = Dense(128, activation='relu')(merged)
output = Dense(10, activation='softmax')(output)

model = Model(inputs=[input_a, input_b], outputs=output)
model.summary()