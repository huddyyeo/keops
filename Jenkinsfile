pipeline {
  agent none 
    stages {
      stage('Build') {
        agent { label 'ubuntu' }
        steps {
          echo 'Building..'
          sh 'git submodule update --init'
          sh 'cd keops/build && cmake ..'
          sh 'cd keops/build && make VERBOSE=0'
        }
      }
      stage('Test') {
        agent { label 'ubuntu' }
        steps {
          echo 'Testing..'
          sh 'git submodule update --init'
          sh 'cd pykeops/test && python3 unit_tests_pytorch.py'
          sh 'cd pykeops/test && python3 unit_tests_numpy.py'
        }
      }
      stage('Build') {
        agent { label 'macos' }
        steps {
          echo 'Building..'
          sh 'git submodule update --init'
          sh 'cd keops/build && cmake ..'
          sh 'cd keops/build && make VERBOSE=0'
        }
      }
      stage('Test') {
        agent { label 'macos' }
        steps {
          echo 'Testing..'
          sh 'git submodule update --init'
          sh 'cd pykeops/test && /Users/ci/miniconda3/bin/python3 unit_tests_pytorch.py'
          sh 'cd pykeops/test && /Users/ci/miniconda3/bin/python3 unit_tests_numpy.py'
      }
    }
  }
}
        