pipeline {
    environment { 
        registry = "prasoonm/python-docker-flask" 
        registryCredential = 'DOCKER_CRED'
        dockerImage = "prasoonm/python-docker-flask"
    }
    agent { 
        node {
        label 'kube'
        }
    }
    stages {
        stage("Code_Fetch"){
            steps{
            git branch: 'main',
            credentialsId: 'github',
            url: 'https://github.com/bcamishrapr/python-app.git'
        }
        
        }
        stage("Docker Build") {
            steps{
                //sh "docker build -t $dockerImage ."
                //sh "docker tag  $dockerImage" $dockerImage
                sh "docker image list|head -n2"
                script { 
                    dockerImage = docker.build registry + ":$BUILD_NUMBER"
                }
        }
        }
        stage("Push Image to Docker-Hub") {
            environment {
                DOCKER_HUB_CRED = credentials('DOCKER_CRED')
            }
            steps{
                
             script { 
                    docker.withRegistry( '', registryCredential ) { 
                        dockerImage.push() 
                   }
                } 
                //sh 'docker login -u prasoonm -p $DOCKER_HUB_CRED_PSW'
                //sh "docker push $dockerImage"
            }
        }
        stage('Cleaning up Docker Image From Local Machine') { 
            steps { 
                sh "docker rmi $registry:$BUILD_NUMBER" 
            }
        } 
        stage("Kubernetes Deployment") {
            steps{
                script {
                    
                //sh "kubectl apply -f kube-deploy.yaml"
                    
                sh "sed 's/%IMG_NAME%/$dockerImage/g'  kube-deploy.yaml >  kube-deploy1.yaml"
                sh "kubectl apply -f kube-deploy1.yaml"    
                //sh "kubectl set image deployment/python-deploy python-docker-flask=$registry:$BUILD_NUMBER"   
                    
               // PY_POD = sh (script: "kubectl get po -l app=python-deploy|awk '{print \$1}'|tail -n 1",returnStdout: true).trim()
               // sh "kubectl delete po $PY_POD --force --grace-period=0"
                    
                 sh "sleep 15&&kubectl get po -l app=python-deploy" 
                
                KUBE_SVC = sh (script: "kubectl get svc python-deploy|awk '{print \$1}'|tail -n1",returnStdout: true).trim()
                
                if (KUBE_SVC == "python-deploy"){
                    echo "Service Already Present"
                    sh "kubectl get svc"
                }
                else {
                    //sh "kubectl expose deploy python-deploy --port=5000 --target-port=5000 --type=NodePort"
                    sh "kubectl apply -f kube-svc.yaml"
                }
                  NODE_IP = sh (script: "hostname --all-ip-addresses|awk '{print\$2}'",returnStdout: true).trim()
                  NODE_PORT = sh (script: "kubectl get svc python-deploy |awk '{print \$5}'|tail -n 1|cut -d : -f2|rev|sed 's|.*/||'|rev",returnStdout: true).trim()
                  echo "VISIT--> http://$NODE_IP:$NODE_PORT"
                }
                
                sh "echo 'DEPLOYMENT DONE'"
            }
        }
    }
}
