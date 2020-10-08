# Test for gaussian kernel operation using LazyTensors.

import time

import math
import torch
from pykeops.torch import LazyTensor

M, N, D, DV = 1000, 1000, 3, 1000


test_grad = True
device_id = 'cuda'
do_warmup = False

x = torch.rand(M, 1, D, device=device_id)/math.sqrt(D)
y = torch.rand(1, N, D, device=device_id)/math.sqrt(D)
b = torch.randn(N, DV, requires_grad=test_grad, device=device_id)

def fun(x,y,b,backend):
    if backend=="keops":
        x = LazyTensor(x)
        y = LazyTensor(y)
    elif backend!="torch":
        raise ValueError("wrong backend")
    Dxy = ((x-y)**2).sum(dim=2) 
    Kxy = (- Dxy).exp() 
    if backend=="keops":
        out = LazyTensor.__matmul__(Kxy,b,optional_flags=['-DUSE_FINAL_CHUNKS=0','-DDIMFINALCHUNK=64'])
    else:
        out = Kxy @ b
    torch.cuda.synchronize() 
    #print("out:",out.flatten()[:10])
    return out
    
backends = ["torch","keops"]
    
out = []
for backend in backends:
    if do_warmup:
        fun(x[:min(M,100),:,:],y[:,:min(N,100),:],b[:min(N,100),:],backend)
        fun(x[:min(M,100),:,:],y[:,:min(N,100),:],b[:min(N,100),:],backend)
    start = time.time()
    out.append(fun(x,y,b,backend).squeeze())
    end = time.time()
    print("time for "+backend+":", end-start )

if len(out)>1:
    print("relative error:", (torch.norm(out[0]-out[1])/torch.norm(out[0])).item() )

if test_grad:
    out_g = []
    for k, backend in enumerate(backends):
        start = time.time()
        out_g.append(torch.autograd.grad((out[k] ** 2).sum(), [b])[0])
        end = time.time()
        print("time for "+backend+" (grad):", end-start )
    
    if len(out_g)>1:
        print("relative error grad:", (torch.norm(out_g[0]-out_g[1])/torch.norm(out_g[0])).item() )
    