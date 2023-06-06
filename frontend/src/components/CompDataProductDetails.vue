<template>
  <div>
    <b-alert variant="warning" v-model="showAlert">
      Computational Data Product is not found!
    </b-alert>
    <div v-if="item">
      <b-container fluid>
        <b-row class="m-4">
          <b-col cols="6">
            <div>
              <b-card class="d-flex justify-content-center align-items-center w-100">
                <b-img fluid :src="structureImg" alt="Structure"/>
              </b-card>
            </div>
          </b-col>

          <b-col cols="6">
            <b-row>
              <b-col cols="8">
                <b-card>
                  <div class="dp-row">
                    <div class="dp-key">Family</div>
                    <div class="dp-value">Family</div>
                  </div>
                  <div class="dp-row">
                    <div class="dp-key">Formula</div>
                    <div class="dp-value">{{ item.emp_formula }}</div>
                  </div>
                  <div class="dp-row">
                    <div class="dp-key">Number of Atoms</div>
                    <div class="dp-value">68</div>
                  </div>
                  <div class="dp-row">
                    <div class="dp-key">Electron Symmetry</div>
                    <div class="dp-value">2-A</div>
                  </div>
                  <div class="dp-row">
                    <div class="dp-key">Charge</div>
                    <div class="dp-value">{{ item.mol_chrg }}</div>
                  </div>
                  <div class="dp-row">
                    <div class="dp-key">Multiplicity</div>
                    <div class="dp-value">2</div>
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
                <b-card style="margin-bottom: 50px;">
                  <div class="dp-row">
                    <div class="dp-key">Project Name</div>
                    <div class="dp-value">{{ item.ProjectName }}</div>
                  </div>
                  <div class="dp-row">
                    <div class="dp-key">Experiment Name</div>
                    <div class="dp-value">{{ item.ExperimentName }}</div>
                  </div>
                  <div class="dp-row">
                    <div class="dp-key">Created by</div>
                    <div class="dp-value">{{ item.Username }}</div>
                  </div>
                  <div class="dp-row">
                    <div class="dp-key">Indexed Time</div>
                    <div class="dp-value">{{ item.IndexedTime }}</div>
                  </div>
                </b-card>
              </b-col>
            </b-row>
          </b-col>
        </b-row>

        <b-row class="m-4">
          <b-col cols="6">
            <b-card v-if="item.ExecutionEnvironment" style="margin-bottom: 50px;">
              <template #header>
                <h4 class="mb-0">Execution Environment</h4>
              </template>
              <div class="dp-row">
                <div class="dp-key">Calc By</div>
                <div class="dp-value">{{ item.ExecutionEnvironment.CalcBy }}</div>
              </div>
              <div class="dp-row">
                <div class="dp-key">Job CPU Run Time</div>
                <div class="dp-value">{{ item.ExecutionEnvironment.JobCPURunTime }}</div>
              </div>
              <div class="dp-row">
                <div class="dp-key">Calc Machine</div>
                <div class="dp-value">{{ item.ExecutionEnvironment.CalcMachine }}</div>
              </div>
              <div class="dp-row">
                <div class="dp-key">Actual Job Run Time</div>
                <div class="dp-value">{{ item.ExecutionEnvironment.ActualJobRunTime }}</div>
              </div>
              <div class="dp-row">
                <div class="dp-key">Fin Time</div>
                <div class="dp-value">{{ item.ExecutionEnvironment.FinTime }}</div>
              </div>
              <div class="dp-row">
                <div class="dp-key">Memory</div>
                <div class="dp-value">{{ item.ExecutionEnvironment.Memory }}</div>
              </div>
              <div class="dp-row">
                <div class="dp-key">NProc Shared</div>
                <div class="dp-value">{{ item.ExecutionEnvironment.NProcShared }}</div>
              </div>
              <div class="dp-row">
                <div class="dp-key">Fin Time Stamp</div>
                <div class="dp-value">{{ item.ExecutionEnvironment.FinTimeStamp }}</div>
              </div>
            </b-card>
          </b-col>
        </b-row>

        <b-row class="m-4" style="padding: 0 15px;">
          <b-card v-if="item.CalculatedProperties" class="full-width">
            <template #header>
              <h4 class="mb-0">Calculated Properties</h4>
            </template>
            <b-row>
              <b-col cols="6">
                <div class="dp-row">
                  <div class="dp-key">Homos</div>
                  <div class="dp-value">{{ item.CalculatedProperties.Homos }}</div>
                </div>
                <div class="dp-row">
                  <div class="dp-key">Dipole X</div>
                  <div class="dp-value">{{ item.CalculatedProperties.Dipole.x }}</div>
                </div>
                <div class="dp-row">
                  <div class="dp-key">Dipole Y</div>
                  <div class="dp-value">{{ item.CalculatedProperties.Dipole.y }}</div>
                </div>
                <div class="dp-row">
                  <div class="dp-key">Dipole Z</div>
                  <div class="dp-value">{{ item.CalculatedProperties.Dipole.z }}</div>
                </div>
                <div class="dp-row">
                  <div class="dp-key">HF</div>
                  <div class="dp-value">{{ item.CalculatedProperties.HF }}</div>
                </div>
                <div class="dp-row">
                  <div class="dp-key">Homo eigenvalue</div>
                  <div class="dp-value">{{ item.CalculatedProperties.HomoEigenvalue }}</div>
                </div>
                <div class="dp-row">
                  <div class="dp-key">Homo eigenvalues</div>
                  <div class="dp-value">
                    <div v-for="(homoEigenvalue, index) in item.CalculatedProperties.HomoEigenvalues" :key="index">
                      {{ homoEigenvalue }}
                    </div>
                  </div>
                </div>
              </b-col>
              <b-col cols="6">
                <div class="dp-row">
                  <div class="dp-key">Lumo eigenvalue</div>
                  <div class="dp-value">{{ item.CalculatedProperties.LumoEigenvalue }}</div>
                </div>
                <div class="dp-row">
                  <div class="dp-key">Lumo eigenvalues</div>
                  <div class="dp-value">
                    <div v-for="(lumoEigenvalue, index) in item.CalculatedProperties.LumoEigenvalues" :key="index">
                      {{ lumoEigenvalue }}
                    </div>
                  </div>
                </div>
              </b-col>
            </b-row>
          </b-card>
        </b-row>

        <b-row class="m-4">
          <b-col cols="6">
            <b-card v-if="item.FinalMoleculeStructuralFormats" style="margin-bottom: 50px;">
              <template #header>
                <h4 class="mb-0">Structural Formats</h4>
              </template>
              <div class="dp-row">
                <div class="dp-key">SDF</div>
                <div class="dp-value">{{ item.FinalMoleculeStructuralFormats.SDF }}</div>
              </div>
              <div class="dp-row">
                <div class="dp-key">PDB</div>
                <div class="dp-value">{{ item.FinalMoleculeStructuralFormats.PDB }}</div>
              </div>
            </b-card>
          </b-col>
        </b-row>

        <b-row class="m-4" style="padding: 0 15px;">
          <b-card v-if="item.Calculation" class="full-width">
            <template #header>
              <h4 class="mb-0">Calculation</h4>
            </template>
            <div class="dp-row">
              <div class="dp-key">JobStatus</div>
              <div class="dp-value">{{ item.Calculation.JobStatus }}</div>
            </div>
            <div class="dp-row">
              <div class="dp-key">Basis</div>
              <div class="dp-value">{{ item.Calculation.Basis }}</div>
            </div>
            <div class="dp-row">
              <div class="dp-key">NMO</div>
              <div class="dp-value">{{ item.Calculation.NMO }}</div>
            </div>
            <div class="dp-row">
              <div class="dp-key">Keywords</div>
              <div class="dp-value">{{ item.Calculation.Keywords }}</div>
            </div>
            <div class="dp-row">
              <div class="dp-key">Package</div>
              <div class="dp-value">{{ item.Calculation.Package }}</div>
            </div>
            <div class="dp-row">
              <div class="dp-key">CalcType</div>
              <div class="dp-value">{{ item.Calculation.CalcType }}</div>
            </div>
            <div class="dp-row">
              <div class="dp-key">Methods</div>
              <div class="dp-value">{{ item.Calculation.Methods }}</div>
            </div>
          </b-card>
        </b-row>

        <b-row class="m-4">
          <b-col cols="6">
            <b-card v-if="item.Identifiers" style="margin-bottom: 50px;">
              <template #header>
                <h4 class="mb-0">Identifiers</h4>
              </template>
              <div class="dp-row">
                <div class="dp-key">InChIKey</div>
                <div class="dp-value">{{ item.Identifiers.InChIKey }}</div>
              </div>
              <div class="dp-row">
                <div class="dp-key">Canonical SMILES</div>
                <div class="dp-value">{{ item.Identifiers.CanonicalSMILES }}</div>
              </div>
              <div class="dp-row">
                <div class="dp-key">InChI</div>
                <div class="dp-value">{{ item.Identifiers.InChI }}</div>
              </div>
              <div class="dp-row">
                <div class="dp-key">SMILES</div>
                <div class="dp-value">{{ item.Identifiers.SMILES }}</div>
              </div>
            </b-card>
          </b-col>
        </b-row>

        <b-row class="m-4" style="padding: 0 15px;">
          <b-card v-if="item.Files" class="full-width">
            <template #header>
              <h4 class="mb-0">Files</h4>
            </template>
            <div class="dp-row">
              <div class="dp-key">SMILES File</div>
              <div class="dp-value">{{ item.Files.SMILESFile }}</div>
            </div>
            <div class="dp-row">
              <div class="dp-key">SDF Structure File</div>
              <div class="dp-value">{{ item.Files.SDFStructureFile }}</div>
            </div>
            <div class="dp-row">
              <div class="dp-key">Gaussian Output File</div>
              <div class="dp-value">{{ item.Files.GaussianOutputFile }}</div>
            </div>
            <div class="dp-row">
              <div class="dp-key">Gaussian Input File</div>
              <div class="dp-value">{{ item.Files.GaussianInputFile }}</div>
            </div>
            <div class="dp-row">
              <div class="dp-key">PDB Structure File</div>
              <div class="dp-value">{{ item.Files.PDBStructureFile }}</div>
            </div>
            <div class="dp-row">
              <div class="dp-key">InChI File</div>
              <div class="dp-value">{{ item.Files.InChIFile }}</div>
            </div>
          </b-card>
        </b-row>

        <b-row class="m-4" style="padding: 0 15px;">
          <b-card v-if="item.InputFileConfiguration" class="full-width">
            <template #header>
              <h4 class="mb-0">Input File Configuration</h4>
            </template>
            <div class="dp-row">
              <div class="dp-key">Link0 Commands</div>
              <div class="dp-value">{{ item.InputFileConfiguration.Link0Commands }}</div>
            </div>
            <div class="dp-row">
              <div class="dp-key">Route Commands</div>
              <div class="dp-value">{{ item.InputFileConfiguration.RouteCommands }}</div>
            </div>
          </b-card>
        </b-row>

      </b-container>
    </div>
  </div>
</template>

<script>
import fallbackStructure from "../assets/images/structure-fallback.svg"

const {utils} = AiravataAPI;

export default {
  props: {
    dp: Object
  },
  data() {
    return {
      item: null,
      showAlert: false,
      structureImg: fallbackStructure
    };
  },
  mounted() {
    if (!this.item) {
      this.fetchData();
    } else {
      this.item = this.dp;
    }
  },
  methods: {
    fetchData() {
      utils.FetchUtils.get(`/smiles/comp-dp/${this.$route.params.id}`)
          .then(response => {
            this.item = response;
          })
          .catch((e) => {
            if (e.details && e.details.status === 404) {
              this.showAlert = true;
              this.redirectToHome();
            }
          });
    },
    redirectToHome() {
      setTimeout(() => {
        this.$router.push({name: 'data-product-list', query: {type: 'comp'}});
      }, 3000);
    }
  }
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

.full-width {
  width: 100vw;
  margin-bottom: 50px;

}
</style>

