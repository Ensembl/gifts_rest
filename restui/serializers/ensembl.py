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

# flatten list of lists, i.e. list of transcripts for each gene

from itertools import chain
from django.utils import timezone
from rest_framework import serializers
from restui.tasks import bulk_upload_task
from restui.models.ensembl import EnsemblTranscript
from restui.models.ensembl import EnsemblSpeciesHistory
from restui.models.ensembl import EnspUCigar

class EnsemblTranscriptSerializer(serializers.Serializer):
    """
    Deserialise transcripts specified in genes
    ensembl/load/<species>/<assembly_accession>/<ensembl_tax_id>/<ensembl_release> endpoint

    NOTE

    - cannot use ModelSerializer, doesn't work with bulk_insert
      must explicity specify serialization fields
    - use null default values so if the client doesn't provide some values
      the defaults override the existing field (otherwise the existing
      value won't be replaced)

    """

    transcript_id = serializers.IntegerField(required=False)
    gene = serializers.PrimaryKeyRelatedField(read_only=True)
    enst_id = serializers.CharField(max_length=30)
    enst_version = serializers.IntegerField(required=False, default=None)
    ccds_id = serializers.CharField(max_length=30, required=False, default=None)
    uniparc_accession = serializers.CharField(max_length=30, required=False, default=None)
    biotype = serializers.CharField(max_length=40, required=False, default=None)
    deleted = serializers.NullBooleanField(required=False, default=None)
    seq_region_start = serializers.IntegerField(required=False, default=None)
    seq_region_end = serializers.IntegerField(required=False, default=None)
    supporting_evidence = serializers.CharField(max_length=45, required=False, default=None)
    userstamp = serializers.CharField(max_length=30, required=False, default=None)
    time_loaded = serializers.DateTimeField(required=False)
    select = serializers.NullBooleanField(required=False, default=None)
    ensp_id = serializers.CharField(max_length=30, required=False, default=None)
    ensp_len = serializers.IntegerField(required=False, default=None)
    source = serializers.CharField(max_length=30, required=False, default=None)


"""
Customizing ListSerializer behaviour

From http://www.django-rest-framework.org/api-guide/serializers/#listserializer

There are a few use cases when you might want to customize the ListSerializer
behaviour. For example:

You want to provide particular validation of the lists, such as checking that
one element does not conflict with another element in a list.

You want to customize the create or update behaviour of multiple objects.

For these cases you can modify the class that is used when many=True is passed,
by using the list_serializer_class option on the serializer Meta class.
"""


class EnsemblGeneListSerializer(serializers.ListSerializer):
    """
    The default implementation for multiple object creation is to simply call
    .create() for each item in the list

    Override using the bulk_insert behaviour from postgres-extra to allow fast
    insertion and return obj IDs so that we can recursively insert gene
    transcripts
    """

    def create(self, validated_data):

        """
        create new species history, use required parameters passed to view from
        endpoint URL
        NOTE: filter is likely to be not necessary
        """
        history_attrs = {}
        for (k, v) in self.context['view'].kwargs.items():
            valid = [
                'species',
                'assembly_accession',
                'ensembl_tax_id',
                'ensembl_release'
            ]

            if k in valid:
                history_attrs[k] = v

        result = bulk_upload_task.delay(history=history_attrs, data=validated_data)

        return result.id, result.status


class EnsemblGeneSerializer(serializers.Serializer):
    gene_id = serializers.IntegerField(required=False)
    ensg_id = serializers.CharField(max_length=30, required=False)
    gene_name = serializers.CharField(max_length=255, required=False, default=None)
    chromosome = serializers.CharField(max_length=50, required=False, default=None)
    region_accession = serializers.CharField(max_length=50, required=False, default=None)
    mod_id = serializers.CharField(max_length=30, required=False, default=None)
    deleted = serializers.NullBooleanField(required=False, default=None)
    seq_region_start = serializers.IntegerField(required=False, default=None)
    seq_region_end = serializers.IntegerField(required=False, default=None)
    seq_region_strand = serializers.IntegerField(required=False, default=None)
    biotype = serializers.CharField(max_length=40, required=False, default=None)
    time_loaded = serializers.DateTimeField(required=False, default=None)
    gene_symbol = serializers.CharField(max_length=30, required=False, default=None)
    gene_accession = serializers.CharField(max_length=30, required=False, default=None)
    source = serializers.CharField(max_length=30, required=False, default=None)

    """
    This is necessary to allow incoming genes data to have a nested list of
    transcripts

    Assume payload always contains non-empty transcripts data for each gene
    (no default value)
    """
    transcripts = EnsemblTranscriptSerializer(many=True, required=False)

    """
    TODO? object-level validation
    http://www.django-rest-framework.org/api-guide/serializers/#validation
    """
    def validate(self, data):
        """
        Check various Gene fields
        """
        return data

    class Meta:
        list_serializer_class = EnsemblGeneListSerializer


class EnspUCigarSerializer(serializers.ModelSerializer):
    """
    Serializer for protein alignment instances
    """

    class Meta:
        model = EnspUCigar
        fields = '__all__'


class EnsemblReleaseSerializer(serializers.Serializer):
    """
    To serialize the latest Ensembl release whose load is complete
    """

    release = serializers.IntegerField(min_value=1, required=True)

class SpeciesHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = EnsemblSpeciesHistory
        fields = '__all__'


class TranscriptSerializer(serializers.ModelSerializer):

    class Meta:
        model = EnsemblTranscript
        fields = '__all__'
