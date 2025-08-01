for suffix in {0..9};
do
	for horizon in 32;
	do
		for n_guide_steps in 2 1
		do
			for scale in 0.1 0.001;
			do
				for t_stopgrad in 4;
				do
								python scripts/plan_guided.py \
									--dataset halfcheetah-medium-v2 \
									--horizon $horizon \
									--n_guide_steps $n_guide_steps \
									--scale $scale \
									--t_stopgrad $t_stopgrad \
									--prefix plans/release \
									--verbose True \
									--suffix $suffix
							done
						done
					done
				done
			done
		done
	done
done

# python plan_guided.py --dataset halfcheetah-medium-v2 \
# --horizon 32 -n_guide_steps 2 --scale 0.1 -t_stopgrad 4 \
# --prefix plans/release --verbose True --suffix 0

# Need to install MuJoCo (linux/mac) from https://github.com/openai/mujoco-py#install-mujoco