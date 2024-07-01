# Calculate Voltage Imbalance
def Calculate_Voltage_Imbalance(VRMS_R: float, VRMS_S: float, VRMS_T: float, VRMS_IMB: float) -> float:

	# Control Variables
	if (VRMS_R is not None and VRMS_S is not None and VRMS_T is not None) and VRMS_IMB is None:
		
		# Calculate Value
		VRMS_Array = [VRMS_R, VRMS_S, VRMS_T]

		# Calculate Value
		AVG_VRMS_Value = sum(VRMS_Array) / len(VRMS_Array)

		# Calculate Deviations
		Deviations = [abs(vrms - AVG_VRMS_Value) for vrms in VRMS_Array]

		# Calculate Max Deviation
		MAX_Deviation = max(Deviations)

		# Calculate Imbalance
		Imbalance = (MAX_Deviation / AVG_VRMS_Value) * 100

		# Return Value
		return Imbalance
