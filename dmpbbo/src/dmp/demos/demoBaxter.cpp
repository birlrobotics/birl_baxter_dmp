/**
 * \file demoDmp.cpp
 * \author Freek Stulp
 * \brief  Demonstrates how to initialize, train and integrate a Dmp.
 *
 * \ingroup Demos
 * \ingroup Dmps
 *
 * This file is part of DmpBbo, a set of libraries and programs for the 
 * black-box optimization of dynamical movement primitives.
 * Copyright (C) 2014 Freek Stulp, ENSTA-ParisTech
 * 
 * DmpBbo is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Lesser General Public License as published by
 * the Free Software Foundation, either version 2 of the License, or
 * (at your option) any later version.
 * 
 * DmpBbo is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Lesser General Public License for more details.
 * 
 * You should have received a copy of the GNU Lesser General Public License
 * along with DmpBbo.  If not, see <http://www.gnu.org/licenses/>.
 */

#include "dmp/Dmp.hpp"
#include "dmp/Trajectory.hpp"

#include "dynamicalsystems/DynamicalSystem.hpp"
#include "dynamicalsystems/ExponentialSystem.hpp"
#include "dynamicalsystems/SigmoidSystem.hpp"
#include "dynamicalsystems/TimeSystem.hpp"
#include "dynamicalsystems/SpringDamperSystem.hpp"

#include "functionapproximators/FunctionApproximatorLWR.hpp"
#include "functionapproximators/MetaParametersLWR.hpp"
#include "functionapproximators/ModelParametersLWR.hpp"

#include "dmpbbo_io/EigenFileIO.hpp"

#include <iostream>
#include <fstream>


using namespace std;
using namespace Eigen;
using namespace DmpBbo;

/** Get a demonstration trajectory.
 * \param[in] ts The time steps at which to sample
 * \return a Demonstration trajectory
 */
Trajectory getDemoTrajectory(const VectorXd& ts);

/** Main function
 * \param[in] n_args Number of arguments
 * \param[in] args Arguments themselves
 * \return Success of exection. 0 if successful.
 */
int main(int n_args, char** args)
{
  string save_directory;
  if (n_args!=2) 
  {
    cerr << "Usage: " << args[0] << "<directory>" << endl;
    return -1;
  }
  save_directory = string(args[1]);

  // READ  TRAJECTORY FROM FILE

  int n_time_steps;    
  //string filename("/home/tony/dmpbbo/dmpbbo_baxter/baxter_raw_data/y_yd_ydd.txt");
  string filename("/home/tony/dmpbbo/dmpbbo_baxter/baxter_raw_data/cartesion_baxter_data.txt");  //for test
  //string filename("/home/tony/dmpbbo/dmpbbo_baxter/baxter_raw_data/test_real_robot.txt");
  Trajectory trajectory = Trajectory::readFromFile(filename);
  int n_dims = trajectory.dim();
  VectorXd ts = trajectory.ts();
  double tau = trajectory.duration();
  
  // MAKE THE FUNCTION APPROXIMATORS
  
  // Initialize some meta parameters for training LWR function approximator
  Eigen::VectorXi n_basis_functions(1);
  n_basis_functions << 11;
  int input_dim = 1;
  double intersection = 0.5;
  MetaParametersLWR* meta_parameters = new MetaParametersLWR(input_dim,n_basis_functions,intersection);      
  FunctionApproximatorLWR* fa_lwr = new FunctionApproximatorLWR(meta_parameters);  
  
  // Clone the function approximator for each dimension of the DMP
  vector<FunctionApproximator*> function_approximators(n_dims);    
  for (int dd=0; dd<n_dims; dd++)
    function_approximators[dd] = fa_lwr->clone();
  
  // CONSTRUCT AND TRAIN THE DMP
  
  // Initialize the DMP
  Dmp* dmp = new Dmp(n_dims, function_approximators, Dmp::KULVICIUS_2012_JOINING);

  // And train it. Passing the save_directory will make sure the results are saved to file.
  bool overwrite = true;
  dmp->train(trajectory,save_directory,overwrite);

  
  // INTEGRATE DMP TO GET REPRODUCED TRAJECTORY
  
  Trajectory traj_reproduced;
  tau = trajectory.duration()+1;
  n_time_steps = 200;
  ts = VectorXd::LinSpaced(n_time_steps,0,tau); // Time steps
  VectorXd y_attr(7);
  VectorXd y_init(7);
  y_init << trajectory.initial_y();
  y_attr<< trajectory.final_y();
  //y_attr<<  0.7075486384121471, -0.5365097805629234,-0.7539515572456809, 0.5882816321540562, 0.5809952234116005, 0.984048675428493, -0.4345000581685434;
  dmp->set_initial_state(y_init);
  dmp->set_attractor_state(y_attr);
  dmp->analyticalSolution(ts,traj_reproduced);

  // Integrate again, but this time get more information
  MatrixXd xs_ana, xds_ana, forcing_terms_ana, fa_output_ana;
  dmp->analyticalSolution(ts,xs_ana,xds_ana,forcing_terms_ana,fa_output_ana);

  
  // WRITE THINGS TO FILE
  trajectory.saveToFile(save_directory,"demonstration_traj.txt",overwrite);
  traj_reproduced.saveToFile(save_directory,"reproduced_traj.txt",overwrite);
    
  MatrixXd output_ana(ts.size(),1+xs_ana.cols()+xds_ana.cols());
  output_ana << xs_ana, xds_ana, ts;
  saveMatrix(save_directory,"reproduced_xs_xds.txt",output_ana,overwrite);
  saveMatrix(save_directory,"reproduced_forcing_terms.txt",forcing_terms_ana,overwrite);
  saveMatrix(save_directory,"reproduced_fa_output.txt",fa_output_ana,overwrite);

  delete meta_parameters;
  delete fa_lwr;
  delete dmp;

  return 0;
}
