"""
.. See the NOTICE file distributed with this work for additional information
   regarding copyright ownership.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

from django.http import Http404

from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.schemas import ManualSchema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


import coreapi
import coreschema

from restui.models.mappings import Alignment
from restui.models.mappings import AlignmentRun
from restui.serializers.alignments import AlignmentSerializer
from restui.serializers.alignments import AlignmentRunSerializer
from restui.pagination import LongResultsPagination



class AlignmentRunCreate(generics.CreateAPIView):
    """
    Store an AlignmentRun
    """
    permission_classes = (IsAuthenticated,)

    serializer_class = AlignmentRunSerializer


class AlignmentRunFetch(generics.RetrieveAPIView):
    """
    Retrieve an AlignmentRun
    """

    queryset = AlignmentRun.objects.all()
    serializer_class = AlignmentRunSerializer


class AlignmentCreate(APIView):
    """
    Insert an Alignment
    """

    permission_classes = (IsAuthenticated,)

    def post(self, request):

        try:
            data = Alignment.objects.get(alignment_run=request.data['alignment_run'],
                                               mapping=request.data['mapping'])
            already_exists = AlignmentSerializer(data)
            return Response(already_exists.data, status=status.HTTP_201_CREATED)
        except Alignment.DoesNotExist:
            serializer = AlignmentSerializer(
                        data={
                            'alignment_run': request.data.get("alignment_run", None),
                            'uniprot_id': request.data.get("uniprot_id", None),
                            'transcript': request.data.get("transcript", None),
                            'mapping':request.data.get("mapping", None),
                            'score1': request.data.get("score1", None),
                            'report': request.data.get("report", None),
                            'is_current': request.data.get("is_current", None),
                            'score2': request.data.get("score2", None)
                        }
                    )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AlignmentFetch(generics.RetrieveAPIView):
    """
    Retrieve an Alignment
    """

    queryset = Alignment.objects.all()
    serializer_class = AlignmentSerializer


class AlignmentByAlignmentRunFetch(generics.ListAPIView):
    """
    Retrieve all alignments for a given alignment run
    """

    serializer_class = AlignmentSerializer
    pagination_class = LongResultsPagination

    schema = ManualSchema(
        description="Retrieve all alignments for a given alignment run",
        fields=[
            coreapi.Field(
                name="id",
                required=True,
                location="path",
                schema=coreschema.Integer(),
                description="Alignmet run id"
            )
        ]
    )

    def get_queryset(self):
        try:
            alignment_run = AlignmentRun.objects.get(pk=self.kwargs["pk"])
        except (AlignmentRun.DoesNotExist, IndexError):
            raise Http404

        mapping_ids = self.request.query_params.get('mapping_id', None)

        if mapping_ids is not None:
            mapping_ids = mapping_ids.split(',')
            return Alignment.objects.filter(alignment_run=alignment_run, mapping_id__in=mapping_ids)
        else:
            return Alignment.objects.filter(alignment_run=alignment_run).order_by('alignment_id')


#
# TODO
#
# We should probably filter to those whose mapping has been completed
# (i.e. MAPPING_COMPLETE in release_mapping_history)
#
class LatestAlignmentsFetch(generics.ListAPIView):
    """
    Retrieve either perfect or blast latest alignments for a given assembly
    """

    serializer_class = AlignmentSerializer
    pagination_class = PageNumberPagination
    schema = ManualSchema(
        description="Retrieve either perfect or blast latest alignments for a given assembly",
        fields=[
            coreapi.Field(
                name="assembly_accession",
                required=True,
                location="path",
                schema=coreschema.String(),
                description="Assembly accession"
            ),
            coreapi.Field(
                name="type",
                location="query",
                schema=coreschema.String(),
                description=(
                    "Type of the alignments to retrieve, either 'perfect_match' "
                    "or 'identity' (default: perfect_match)"
                )
            )
        ]
    )

    def get_queryset(self):
        assembly_accession = self.kwargs["assembly_accession"]

        # alignment type must be either 'identity' or 'perfect_match', default to latter
        alignment_type = self.request.query_params.get('type', 'perfect_match')
        if alignment_type not in ('identity', 'perfect_match'):
            raise Http404('Invalid alignment type')

        try:
            alignment_run = AlignmentRun.objects.filter(
                release_mapping_history__ensembl_species_history__assembly_accession__iexact=assembly_accession,  # pylint: disable=line-too-long
                score1_type=alignment_type
            ).latest('alignment_run_id')
        except (AlignmentRun.DoesNotExist, IndexError):
            raise Http404

        return Alignment.objects.filter(
            alignment_run=alignment_run
        ).order_by('alignment_id')
