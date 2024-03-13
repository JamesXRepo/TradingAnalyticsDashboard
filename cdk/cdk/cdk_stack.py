from aws_cdk import (
    Stack,
    aws_ecr as _ecr, RemovalPolicy
)
from constructs import Construct

class EcrStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope,  id, **kwargs)

        plotly_dash_repository = _ecr.Repository(self, "PlotlyDash",
                                                       repository_name="plotly-dash",
                                                       removal_policy=RemovalPolicy.DESTROY,
                                                       image_tag_mutability=_ecr.TagMutability.IMMUTABLE,
                                                 )
        self._output_props = {
            'plotly_dash_repository': plotly_dash_repository
        }

    @property
    def outputs(self):
        return self._output_props
