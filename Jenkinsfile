pipeline {
    environment { 
        registry = "YourDockerhubAccount/YourRepository" 
        registryCredential = 'DOCKERHUB_CRED'
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
                sh "docker build -t python-docker-dev ."
                sh "docker tag python-docker-dev $dockerImage"
                sh "docker image list|head -n2"
                //sh "docker push $dockerImage"
             
               //sh "docker login -u prasoonm -p $DOCKERHUB_CRED"
        }
        }
        stage("Push Image to Docker-Hub") {
            environment {
                DOCKER_HUB_CRED = credentials('DOCKER_CRED')
            }
            steps{
                sh 'docker login -u prasoonm -p $DOCKER_HUB_CRED_PSW'
                sh "docker push $dockerImage"
            }
        }
        stage("Kubernetes Deployment") {
            steps{
                //sh "kubectl delete deploy python-deploy"
                //sh "kubectl create deploy python-deploy --image=prasoonm/python-docker-flask"
                sh "kubectl apply -f kube-deploy.yaml"
                script {
                KUBE_SVC = sh (script: "kubectl get svc python-deploy|awk '{print \$1}'|tail -n1",returnStdout: true).trim()
                
                if (KUBE_SVC == "python-deploy"){
                    echo "Service Already Present"
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
