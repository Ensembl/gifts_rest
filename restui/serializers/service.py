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
import re

from rest_framework import serializers

from restui.models import EnsemblSpeciesHistory, ReleaseMappingHistory, AlignmentRun


class StatusSerializer(serializers.Serializer):
    """
    Status serializer
    """
    ping = serializers.IntegerField()


class ServiceFlagSerializer(serializers.Serializer):

    ensembl_load_running = serializers.BooleanField()
    uniprot_load_running = serializers.BooleanField()
    ensembl_alignments_runnning = serializers.BooleanField()

    def to_representation(self, instance=None):
        latest_ensembl = EnsemblSpeciesHistory.objects.latest('ensembl_release')
        latest_uniprot = ReleaseMappingHistory.objects.all().latest('uniprot_release')
        ensembl_status = EnsemblSpeciesHistory.objects.filter(ensembl_release=latest_ensembl.ensembl_release)
        uniprot_status = ReleaseMappingHistory.objects.filter(uniprot_release=latest_uniprot.uniprot_release)

        flag_ensembl_load = any([(e.status != 'LOAD_COMPLETE') for e in ensembl_status])
        flag_uniprot_load = any([(e.status != 'MAPPING_COMPLETED') for e in uniprot_status])

        flag_alignments_load = False
        if any([(e.alignment_status != 'ALIGNMENT_COMPLETED') for e in ensembl_status]):
            if AlignmentRun.objects.filter(ensembl_release=latest_ensembl.ensembl_release).exists():
                flag_alignments_load = True
        else:
            flag_alignments_load = False


        return super().to_representation({
            'ensembl_load_running': flag_ensembl_load,
            'uniprot_load_running': flag_uniprot_load,
            'ensembl_alignments_runnning': flag_alignments_load
        })
