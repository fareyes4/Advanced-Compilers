Franz Reyes

this is my dataflow analyses hw for bril. i did reaching definitions and available expressions. both use the worklist code in df.py. they read a bril program and print the in and out sets for each basic block.

what’s here
- reachingdefs.py
- availableexprs.py
- df.py
- tests-rd folder with rd1.bril rd1.out turnt.toml
- tests-ae folder with ae1.bril ae1.out turnt.toml
- DataflowAnalyses_FranzReyes.docx with answers for q1 and q2

how to run with turnt
cd tests-rd
turnt --save rd1.bril
turnt rd1.bril

cd ../tests-ae
turnt --save ae1.bril
turnt ae1.bril

how to run directly
bril2json < tests-rd/rd1.bril | python3 reachingdefs.py
bril2json < tests-ae/ae1.bril | python3 availableexprs.py

note
i used chatgpt to help fix some testing mistakes and some ubuntu errors.

