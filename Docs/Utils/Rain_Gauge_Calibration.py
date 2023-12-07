# Include Libraries
import math

# Variables
Funnel_Dimension = 15.7 # cm
Funnel_Area = math.pi * ((Funnel_Dimension / 2) ** 2) # cm2
Bucket_Size = 3.12 # 4 ml per tip

# Calculations
Multiplier = (Bucket_Size * 10000 / Funnel_Area) / 1000 # mm

# Print
print (f"R:{Funnel_Dimension}cm / A:{Funnel_Area}cm2 / Bucket: {Bucket_Size} --> Multiplier: {Multiplier}")
