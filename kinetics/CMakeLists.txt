include_directories(../msg)
include_directories(../basecode ../utility)
add_library(kinetics
	PoolBase.cpp	
	Pool.cpp	
	BufPool.cpp	
	FuncPool.cpp	
	ReacBase.cpp	
	Reac.cpp	
	EnzBase.cpp	
	CplxEnzBase.cpp	
	Enz.cpp	
	MMenz.cpp	
	Species.cpp	
	ReadKkit.cpp	
	WriteKkit.cpp	
	ReadCspace.cpp	
	SumTotalTerm.cpp	
	MathFuncTerm.cpp	
	FuncBase.cpp	
	MathFunc.cpp	
	SumFunc.cpp	
	lookupVolumeFromMesh.cpp	
	testKinetics.cpp	
        )
target_link_libraries(kinetics basecode)
