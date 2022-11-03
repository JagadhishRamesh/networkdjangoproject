class ComplianceTypeChoices:
	Grn200Lo200 = 'Grn200Lo200'
	Grn200NoLo200 = 'Grn200NoLo200'
	NoGrn200Lo200 = 'NoGrn200Lo200'
	NoGrn200NoLo200 = 'NoGrn200NoLo200'
	TYPE_CHOICES = [
		(Grn200Lo200, 'Has Grn200 vrf and has L200'),
		(Grn200NoLo200, 'Has Grn200 vrf and No L200'),
		(NoGrn200Lo200, 'No Grn200 vrf but has L200'),
		(NoGrn200NoLo200, 'No Grn200 vrf and No L200')
	]