# Score-lit

This is a play app created to track my sheet music library using [streamlit][streamlit-io].

## To do

- [ ] More data
- [ ] Read data from S3 bucket
- [ ] CloudFormation script to deploy
    - [ ] Security group for http/non-standard port

If successful, consider:
- [ ] Get domain (via Route53)
- [ ] Add load-balancer and https to Cloud formation

Docs to aid this:

- Guides for [EC2 deployment][streamlit-deploy], old version of console, perhaps worth a blog post
- How to create a HTTPS load balancer with [Route 53][route53-cert]

## Developer setup

```bash
$ git clone git@github.com:keiranmraine/score-lit.git
$ cd score-lit
$ git hf init # optional, see https://github.com/datasift/gitflow
$ python -m venv .venv
# windows-bash
$ . .venv/Scripts/activate
# linux/mac
$ source .venv/bin/activate
$ pip install streamlit plotly-express
$ streamlit run score.py
```

<!-- references -->
[streamlit-io]: https://streamlit.io/
[route53-cert]: https://levelup.gitconnected.com/get-https-how-to-get-ssl-tls-certificate-in-aws-for-ec2-hosted-application-8d14771a6ff6
[streamlit-deploy]: https://discuss.streamlit.io/t/streamlit-deployment-guide-wiki/5099