pipeline {
    agent { 
        node {
        label 'kube'
        }
    }
    stages {
        stage("Code_Fetch"){
            steps{
            git branch: 'main',
            url: 'https://github.com/bcamishrapr/python-app.git'
        }
        
        }
        stage("Docker Build") {
            steps{
                sh "docker build -t python-docker-dev ."
                sh "docker tag python-docker-dev prasoonm/python-docker-flask"
                sh "docker push prasoonm/python-docker-flask"
            }
        }
        stage("Kubernetes Deployment") {
            steps{
                sh "kubectl delete deploy python-deploy"
                sh "kubectl create deploy python-deploy --image=prasoonm/python-docker-flask"
                //sh "kubectl set image deployments/python-deploy "
                script {
                KUBE_SVC = sh (script: "kubectl get svc python-deploy|awk '{print \$1}'|tail -n1",returnStdout: true).trim()
                
                if (KUBE_SVC == "python-deploy"){
                    echo "Service Already Present"
                }
                else {
                    sh "kubectl expose deploy python-deploy --port=5000 --target-port=5000 --type=NodePort"
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
