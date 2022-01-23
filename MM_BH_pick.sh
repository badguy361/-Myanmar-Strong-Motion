year=2016
mon=05
num=1

w_dir=/home/ncu107602531/CWB_picking_4/picking
d_dir=${w_dir}/MM_${year}_events_HN/${mon}
o_dir=${w_dir}/MM_events_${year}

cd ${d_dir} #enter {d_dir}

sac << END > dummy 
r MM_KTN_HNZ_20160517164855_5182994_RespRemoved.sac MM_KTN_HNE_20160517164855_5182994_RespRemoved.sac MM_KTN_HNN_20160517164855_5182994_RespRemoved.sac
qdp of
ppk m
w over
q
END
