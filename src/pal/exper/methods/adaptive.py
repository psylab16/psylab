# -*- coding: utf-8 -*-

# Copyright (c) 2008-2010 Christopher Brown; All Rights Reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in
#      the documentation and/or other materials provided with the distribution
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# Comments and/or additions are welcome (send e-mail to: c-b@asu.edu).
#

'''Adaptive tracking method

'''

class dynamic:
    name = ''          # Name of the dynamic variable
    steps = [0, 0]     # Stepsizes to use at each reversal (len = #revs)
    downs = 2          # Number of 'downs'
    ups = 1            # Number of 'ups'
    msg = ''           # Description of why the block ended
    val_start = 0      # Starting value
    val_floor = 0      # Floor
    val_ceil = 0       # Ceiling
    val_floor_count = 0# Number of consecutive floor trials
    val_ceil_count = 0 # Number of consecutive ceiling trials
    val_floor_n = 3    # Number of consecutive floor values to quit at
    val_ceil_n = 3     # Number of consecutive ceiling values to quit at
    run_n_trials = 0   # Set to non-zero to run exactly that number of trials
    max_trials = 0     # Maximum number of trials to run
    value = 0          # Current dynamic value
    values = []        # Array of values
    values_track = []  # 0 = no change, -1 = reversal/dn, 1 = reversal/up
    values_rev = []    # Current reversal count
    prev_dir = 0       # Previous direction; -1 = dn, 1 = up
    init_dir = 0       # Initial direction; -1 = dn, 1 = up
    cur_ups = 0        # Counter for current number of ups
    cur_dns = 0        # Counter for current number of downs
    cur_step = 0       # Whether to step this trial; -1 = dn, 1 = up, 0 = none

    def step(cur_step,exp,run,stim,var,user):
        if cur_step == -1:
            var.dynamic.value -= var.dynamic.steps[var.dynamic.reversal]
        elif cur_step == 1:
            var.dynamic.value += var.dynamic.steps[var.dynamic.reversal]


    def track(correct, exp,run,stim,var,user):
        '''correct should a simple bool
        '''
        var.dynamic.values.append(var.dynamic.value)
        if correct:
            var.dynamic.cur_dns += 1                        # Increment dns
            var.dynamic.cur_ups = 0                         # Reset ups
            if var.dynamic.cur_dns == var.dynamic.dns:      # If we have the right number of dns
                var.dynamic.cur_step = -1                   #  Set current step
                var.dynamic.cur_dns = 0                     #  Reset dns
                if var.dynamic.prev_dir == -1:              #  If previous direction was dn
                    var.dynamic.values_track.append(0)      #   No reversal
                elif var.dynamic.prev_dir == 0:             #  If no previous direction (must be start)
                    var.dynamic.prev_dir = -1               #   Set prev_dir
                    var.dynamic.values_track.append(0)      #   Don't record this as a change
                    var.dynamic.init_dir = -1               #   Set initial direction
                else:                                       #  Otherwise, its a reversal
                    var.dynamic.prev_dir = -1               #   Set prev_dir
                    var.dynamic.values_track.append(-1)     #   Record reversal
                    var.dynamic.values_rev.append(var.dynamic.value)
            else:
                var.dynamic.cur_step = 0                    #  No current step
        else:
            var.dynamic.cur_dns = 0                         # Reset dns
            var.dynamic.cur_ups += 1                        # Increment ups
            if var.dynamic.cur_ups == var.dynamic.ups:      # If we have the right number of ups
                var.dynamic.cur_step = 1                    #  Set current step
                var.dynamic.cur_ups = 0                     #  Reset ups
                if var.dynamic.prev_dir == 1:               #  If previous direction was up
                    var.dynamic.values_track.append(0)      #   No reversal
                elif var.dynamic.prev_dir == 0:             #  If no previous direction (must be start)
                    var.dynamic.prev_dir = 1                #   Set prev_dir
                    var.dynamic.values_track.append(0)      #   Don't record this as a change
                    var.dynamic.init_dir = 1                #   Set initial direction
                else:                                       #  Otherwise, its a reversal
                    var.dynamic.prev_dir = 1                #   Set prev_dir
                    var.dynamic.values_track.append(1)      #   Record reversal
                    var.dynamic.values_rev.append(var.dynamic.value)
            else:
                var.dynamic.cur_step = 0                    #  No current step


    def finish_trial(exp, run, var, stim, user):
        '''Check for various end-of-block situations
        '''
        var.dynamic.value = max(var.dynamic.value, var.dynamic.val_floor)
        if var.dynamic.value == var.dynamic.val_floor:
            var.dynamic.val_floor_count += 1
            if var.dynamic.val_floor_count == var.dynamic.val_floor_n:
                run.block_on = False
                var.dynamic.msg = '%g consecutive floor trials reached' % var.dynamic.val_floor_n
        else:
            var.dynamic.val_floor_count = 0
        var.dynamic.value = min(var.dynamic.value, var.dynamic.val_ceil)
        if var.dynamic.value == var.dynamic.val_ceil:
            var.dynamic.val_ceil_count += 1
            if var.dynamic.val_ceil_count == var.dynamic.val_ceil_n:
                run.block_on = False
                var.dynamic.msg = '%g consecutive ceiling trials reached' % var.dynamic.val_ceiling_n
        else:
            var.dynamic.val_ceil_count = 0

        if run.block_on:
            if var.dynamic.run_n_trials > 0 and run.trials == var.dynamic.run_n_trials:
                run.block_on = False
                var.dynamic.msg = '%g trials reached' % var.dynamic.run_n_trials
            elif var.dynamic.max_trials > 0 and run.trials == var.dynamic.max_trials:
                run.block_on = False
                var.dynamic.msg = 'A maximum of %g trials reached' % var.dynamic.max_trials
            elif len(var.dynamic.values_rev) == len(var.dynamic.steps):
                run.block_on = False
                var.dynamic.msg = '%g reversals reached' % var.dynamic.val_floor_n

def pre_exp(exp, run, var, stim, user):
    pass

def post_exp(exp, run, var, stim, user):
    pass

def post_trial(exp, run, var, stim, user):
    '''Move this function to settingsfile
    '''
    var.dynamic.track(run.response==user.interval, exp, run, var, stim, user)
    var.dynamic.step(var.dynamic.cur_step, exp, run, var, stim, user)
    var.dynamic.finish_trial(exp, run, var, stim, user)

    run.trial_on = False