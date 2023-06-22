<template>
  <div>
    <div v-if="record">
      <b-container fluid>
        <b-row class="m-4">
          <b-col cols="6" class="d-flex">
            <b-card class="d-flex justify-content-center align-items-center w-100 h-100 m-0 p-0">
              <molecular-structure-img :structure="record.structure" fit-to-content/>
            </b-card>
          </b-col>

          <b-col cols="6">
            <b-row>
              <b-col cols="8">
                <b-card>
                  <div class="dp-row">
                    <div class="dp-key">Family</div>
                    <div class="dp-value">{{ record.dye_family }}</div>
                  </div>
                  <div class="dp-row">
                    <div class="dp-key">SMILES</div>
                    <div class="dp-value">{{ record.smiles }}</div>
                  </div>
                  <div class="dp-row">
                    <div class="dp-key">Names</div>
                    <div class="dp-value">
                      <div v-for="(name, index) in record.other_names" :key="index">
                        {{ name }}
                      </div>
                    </div>
                  </div>
                </b-card>
              </b-col>
              <b-col cols="4">
                <b-card>
                  <div class="font-weight-bold" style="margin-bottom: 10px;">Related Data</div>
                  <a href="url">Molecule 1 V1</a><br/>
                  <a href="url">Molecule 1 V2</a>
                </b-card>
              </b-col>
            </b-row>
            <b-row>
              <b-col>

              </b-col>
            </b-row>
          </b-col>
        </b-row>

        <b-row class="m-4">
          <b-col cols="6">
            <b-card v-if="record.electrochemical_potentials" class="card-component">
              <template #header>
                <h4 class="mb-0">Electro Chemical Potentials</h4>
              </template>
              <div class="dp-row">
                <div class="dp-key">Value Quoted Ref</div>
                <div class="dp-value">{{ record.electrochemical_potentials.value_quoted_ref }}</div>
              </div>
              <div class="dp-row">
                <div class="dp-key">Method</div>
                <div class="dp-value">{{ record.electrochemical_potentials.method }}</div>
              </div>
              <div class="dp-row">
                <div class="dp-key">Temperature</div>
                <div class="dp-value">{{ record.electrochemical_potentials.temperature }}</div>
              </div>
              <div class="dp-row">
                <div class="dp-key">Human Validator</div>
                <div class="dp-value">{{ record.electrochemical_potentials.human_validator }}</div>
              </div>
            </b-card>
          </b-col>
        </b-row>

        <b-row class="m-4">
          <b-col cols="6">
            <b-card v-if="record.fluorescence_lifetimes" class="card-component">
              <template #header>
                <h4 class="mb-0">Fluorescence Lifetime</h4>
              </template>
              <div class="dp-row">
                <div class="dp-key">Solvent</div>
                <div class="dp-value">{{ record.fluorescence_lifetimes.solvent }}</div>
              </div>
              <div class="dp-row">
                <div class="dp-key">Temperature</div>
                <div class="dp-value">{{ record.fluorescence_lifetimes.temperature }}</div>
              </div>
              <div class="dp-row">
                <div class="dp-key">Units</div>
                <div class="dp-value">{{ record.fluorescence_lifetimes.units }}</div>
              </div>
              <div class="dp-row">
                <div class="dp-key">Value</div>
                <div class="dp-value">{{ record.fluorescence_lifetimes.value }}</div>
              </div>
            </b-card>
          </b-col>
        </b-row>

        <b-row class="m-4">
          <b-col cols="6">
            <b-card v-if="record.spectral_data" class="card-component">
              <template #header>
                <h4 class="mb-0">Spectral Data</h4>
              </template>
              <div class="dp-row">
                <div class="dp-key">Solvent</div>
                <div class="dp-value">{{ record.spectral_data.solvent }}</div>
              </div>
              <div class="dp-row">
                <div class="dp-key">Absorb Max</div>
                <div class="dp-value">{{ record.spectral_data.absorb_max }}</div>
              </div>
              <div class="dp-row">
                <div class="dp-key">Emission Max</div>
                <div class="dp-value">{{ record.spectral_data.emis_max }}</div>
              </div>
              <div class="dp-row">
                <div class="dp-key">Quantum Yield</div>
                <div class="dp-value">{{ record.spectral_data.quantum_yield }}</div>
              </div>
              <div v-if="record.spectral_data.emisn_spectra">
                <div class="dp-row">
                  <div class="dp-key">Emission Spectra</div>
                </div>
                <div>
                  <div class="dp-row">
                    <div class="nested-key">Solvent</div>
                    <div class="nested-value">{{ record.spectral_data.emisn_spectra.solvent }}</div>
                  </div>
                  <div class="dp-row">
                    <div class="nested-key">Temperature</div>
                    <div class="nested-value">{{ record.spectral_data.emisn_spectra.temperature }}</div>
                  </div>
                  <div class="dp-row">
                    <div class="nested-key">Temperature Units</div>
                    <div class="nested-value">{{ record.spectral_data.emisn_spectra.temperature_units }}</div>
                  </div>
                </div>
              </div>
              <div v-if="record.spectral_data.absorp_spectra">
                <div class="dp-row">
                  <div class="dp-key">Absorp Spectra</div>
                </div>
                <div>
                  <div class="dp-row">
                    <div class="nested-key">Solvent</div>
                    <div class="nested-value">{{ record.spectral_data.absorp_spectra.solvent }}</div>
                  </div>
                  <div class="dp-row">
                    <div class="nested-key">Temperature</div>
                    <div class="nested-value">{{ record.spectral_data.absorp_spectra.temperature }}</div>
                  </div>
                  <div class="dp-row">
                    <div class="nested-key">Temperature Units</div>
                    <div class="nested-value">{{ record.spectral_data.absorp_spectra.temperature_units }}</div>
                  </div>
                </div>
              </div>

            </b-card>
          </b-col>
        </b-row>

      </b-container>
    </div>
  </div>
</template>

<script>
import MolecularStructureImg from "@/components/common/MolecularStructureImg";

export default {
  props: {
    record: {
      type: Object,
      required: true,
    },
  },
  components: {
    MolecularStructureImg
  },
  data() {
    return {
      showAlert: false
    };
  },
  methods: {}
}
</script>

<style scoped>

.dp-row {
  display: flex;
  flex-direction: row;
  margin-bottom: 5px;
}

.dp-key {
  flex: 1;
  font-weight: bold;
}

.dp-value {
  flex: 1;
  color: #666;
}

.nested-key {
  flex: 1;
  margin-left: 20px;
}

.nested-value {
  flex: 1;
  color: #666;
}

.card-component {
  margin-bottom: 20px;
}

</style>

