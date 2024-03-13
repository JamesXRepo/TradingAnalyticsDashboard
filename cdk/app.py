#!/usr/bin/env python3
import os

import aws_cdk as cdk

from plotly_dash_ecs.alb_stack import AlbStack
from plotly_dash_ecs.cluster_stack import ClusterStack
from plotly_dash_ecs.dash_app_service import DashAppService
from plotly_dash_ecs.ecr_stack import EcrStack
from plotly_dash_ecs.s3_stack import S3Stack
from plotly_dash_ecs.vpc_stack import VpcStack

app = cdk.App()
environment = cdk.Environment(account='<your AWS account ID>', region='<the desired AWS region>')

tagsInfra = {
  "cost": "PlotlyDashInfra",
  "team": "SiecolaCode"
}

tagsPlotlyDashApp = {
  "cost": "PlotlyDashApp",
  "team": "SiecolaCode"
}

ecr_stack = EcrStack(app, "Ecr",
                     env=environment,
                     tags=tagsInfra
                     )

vpc_stack = VpcStack(app, "Vpc",
                     env=environment,
                     tags=tagsInfra
                     )

cluster_stack = ClusterStack(app, "Cluster",
                             env=environment,
                             tags=tagsInfra,
                             props=vpc_stack.outputs
                             )
cluster_stack.add_dependency(vpc_stack)

alb_stack = AlbStack(app, "ALB",
                     env=environment,
                     tags=tagsInfra,
                     props=vpc_stack.outputs
                     )
alb_stack.add_dependency(vpc_stack)

s3_stack = S3Stack(app, "Bucket",
                   env=environment,
                   tags=tagsInfra
                   )

dash_app_service_props = {}
dash_app_service_props.update(ecr_stack.outputs)
dash_app_service_props.update(vpc_stack.outputs)
dash_app_service_props.update(cluster_stack.outputs)
dash_app_service_props.update(alb_stack.outputs)
dash_app_service_props.update(s3_stack.outputs)
dash_app_service_stack = DashAppService(app, "DashAppService",
                                        env=environment,
                                        tags=tagsPlotlyDashApp,
                                        props=dash_app_service_props)
dash_app_service_stack.add_dependency(ecr_stack)
dash_app_service_stack.add_dependency(vpc_stack)
dash_app_service_stack.add_dependency(cluster_stack)
dash_app_service_stack.add_dependency(alb_stack)

app.synth()
