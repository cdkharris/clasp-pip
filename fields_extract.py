'''
Camilla Harris
February 2018
A script for extracting and calculating EM fields on a cartesian grid.

  1  load data
  2  load equations to go from GSE to EpO, and to calculate E = -v x B
  3  create rectangular zone for the data of interest
  4  interpolate E and B onto zone
  5  write data as whitespace-delimited tecplot output

'''

import tecplot
import numpy as np
import os

def fields_extract(dataname,xmin,xmax,ymin,ymax,zmin,zmax,h,savename):
    '''
    This loads the Tecplot data, then calls the rest of the functions defined below.
    '''
    batsrus = tecplot.data.load_tecplot(dataname)
    print('fields_extract: '+ dataname +' loaded!')
    load_eqns()
    create_zone(batsrus,xmin,xmax,ymin,ymax,zmin,zmax,h)
    interpolate()
    write_data(batsrus,savename)

def load_eqns():
    '''
    This loads equations to transform from GSE to EPhiO and calculate electric field.
    '''
    eqnstrx  = '{X [R]} = -1*{X [R]}'
    eqnstry  = '{Y [R]} = -1*{Y [R]}'
    eqnstrbx = '{B_x [nT]} = -1*{B_x [nT]}'
    eqnstrby = '{B_y [nT]} = -1*{B_y [nT]}'
    eqnstrux = '{U_x [km/s]} = -1*{U_x [km/s]}'
    eqnstruy = '{U_y [km/s]} = -1*{U_y [km/s]}'
    eqnstrex = '{E_x [V m-1]} = -1*1e-6*({U_y [km/s]}*{B_z [nT]} - {U_z [km/s]}*{B_y [nT]})'
    eqnstrey = '{E_y [V m-1]} = -1*1e-6*({U_z [km/s]}*{B_x [nT]} - {U_x [km/s]}*{B_z [nT]})'
    eqnstrez = '{E_z [V m-1]} = -1*1e-6*({U_x [km/s]}*{B_y [nT]} - {U_y [km/s]}*{B_x [nT]})'
    tecplot.data.operate.execute_equation(eqnstrx)
    tecplot.data.operate.execute_equation(eqnstry)
    tecplot.data.operate.execute_equation(eqnstrbx)
    tecplot.data.operate.execute_equation(eqnstrby)
    tecplot.data.operate.execute_equation(eqnstrux)
    tecplot.data.operate.execute_equation(eqnstruy)
    tecplot.data.operate.execute_equation(eqnstrex)
    tecplot.data.operate.execute_equation(eqnstrey)
    tecplot.data.operate.execute_equation(eqnstrez)
    print('fields_extract: equations loaded!')

def create_zone(batsrus,xmin,xmax,ymin,ymax,zmin,zmax,h):
    '''
    This takes two 3D points and a grid spacing to calculate a cartesian grid to extract data on.
    Right now it extracts a 3D rectangular axis-aligned volume; it could be adapted further to do arbitrary 2D cuts.
    '''
    ## calculate I, J, K for given resolution
    i = int((xmax-xmin)/h) + 1
    j = int((ymax-ymin)/h) + 1
    k = int((zmax-zmin)/h) + 1
    shape = i*j*k

    print('fields_extract: i {} j {} k {} shape {}'.format(i,j,k,shape))

    ## get the points in X, Y, Z
    x = np.linspace(xmin,xmax,i)
    y = np.linspace(ymin,ymax,j)
    z = np.linspace(zmin,zmax,k)
    points = np.ones([shape,3])
    count = 0
    for ii in range(i):
        for jj in range(j):
            for kk in range(k):
                points[ii*j*k+jj*k+kk,:] = np.array([x[ii],y[jj],z[kk]])

    ## create zone
    section = batsrus.add_ordered_zone('EPhiO, xmin {}, xmax {}, ymin {}, ymax {}, zmin {}, zmax {}, h {}'.format(xmin,xmax,ymin,ymax,zmin,zmax,h),shape)
    section.values('X [[]R[]]')[:] = points[:,0]
    section.values('Y [[]R[]]')[:] = points[:,1]
    section.values('Z [[]R[]]')[:] = points[:,2]
    print('fields_extract: rect zone created!')

def interpolate():
    '''
    This calls Tecplot's interpolate function on the new zone.
    '''
    tecplot.data.operate.interpolate_linear(1,0)
    print('fields_extract: interpolated!')

def write_data(batsrus,savename):
    '''
    This exports the data to a text file.
    '''
    varnames = ('X [[]R[]]','Y [[]R[]]','Z [[]R[]]',
                'B_x [[]nT[]]','B_y [[]nT[]]','B_z [[]nT[]]',
                'E_x [[]V m-1[]]','E_y [[]V m-1[]]','E_z [[]V m-1[]]')
    variables_to_save = [batsrus.variable(V) for V in varnames]
    tecplot.data.save_tecplot_ascii(savename, dataset=batsrus,
                                    variables=variables_to_save,
                                    zones=1, use_point_format = True)
    print('fields_extract: ' + savename + ' saved!')

## The points defining the region to extract on
xmin = -5; ymin = -5; zmin = -15
xmax = 15; ymax = 5; zmax = 15
## The grid spacing, in planetary radii
h = 1.0
## The data to extract from
dirname  = 'absolute/path/to/dir'
filename = 'name_of_3D_tecplot_data.plt'

savename = os.path.join(dirname,filename[0:-4]+'_x_{}_{}_y_{}_{}_z_{}_{}_h_{}.dat'.format(xmin,xmax,ymin,ymax,zmin,zmax,h))
fields_extract(os.path.join(dirname,filename),xmin,xmax,ymin,ymax,zmin,zmax,h,savename)
