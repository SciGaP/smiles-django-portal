<template>
  <div>
    <b-alert variant="warning" v-model="showAlert">
      Computational Data Product is not found!
    </b-alert>


    <div class="layout-container">
      <!-- Left Sidebar Navigation -->
      <div class="navigation">
        <h2>{{ item.name }}</h2>
        <nav class="side-nav">
          <ul>
            <!-- Navigation Items -->
            <li v-for="section in sections" :key="section.id" :class="{ active: currentSection === section.id }">
              <a href="#" @click.prevent="scrollToSection(section.id)">
                {{ section.label }}
              </a>
            </li>
          </ul>
        </nav>
      </div>

      <!-- Right-Side Data Details -->
      <div class="details-content">
        <div v-if="item">
          <b-container fluid>
            <b-row id="summary" class="m-4">
              <b-col cols="6" class="d-flex">
                <b-card class="d-flex justify-content-center align-items-center w-100 h-100 m-0 p-0">
                  <molecular-structure-img :structure="item.structure" fit-to-content/>
                </b-card>
              </b-col>

              <b-col cols="6">
                <b-row>
                  <b-col cols="8">
                    <b-card>
                      <div class="dp-row">
                        <div class="dp-key">Family</div>
                        <div class="dp-value">{{ item.dye_family }}</div>
                      </div>
                      <div class="dp-row">
                        <div class="dp-key">Names</div>
                        <div class="dp-value">
                          <div v-for="(name, index) in item.other_names" :key="index">
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
                    <b-card class="card-component">
                      <div class="dp-row">
                        <div class="dp-key">Project Name</div>
                        <div class="dp-value">{{ item.project_name }}</div>
                      </div>
                      <div class="dp-row">
                        <div class="dp-key">Experiment Name</div>
                        <div class="dp-value">{{ item.experiment_name }}</div>
                      </div>
                      <div class="dp-row">
                        <div class="dp-key">Created by</div>
                        <div class="dp-value">{{ item.username }}</div>
                      </div>
                      <div class="dp-row">
                        <div class="dp-key">Indexed Time</div>
                        <div class="dp-value">{{ item.indexed_time }}</div>
                      </div>
                    </b-card>
                  </b-col>
                </b-row>
              </b-col>
            </b-row>

            <b-row id="execution-environment" class="m-4">
              <b-col cols="6">
                <b-card v-if="item.execution_environment" class="card-component">
                  <template #header>
                    <h4 class="mb-0">Execution Environment</h4>
                  </template>
                  <div class="dp-row">
                    <div class="dp-key">Calc By</div>
                    <div class="dp-value">{{ item.execution_environment.calc_by }}</div>
                  </div>
                  <div class="dp-row">
                    <div class="dp-key">Job CPU Run Time</div>
                    <div class="dp-value">{{ item.execution_environment.job_cpu_runtime }}</div>
                  </div>
                  <div class="dp-row">
                    <div class="dp-key">Calc Machine</div>
                    <div class="dp-value">{{ item.execution_environment.calc_machine }}</div>
                  </div>
                  <div class="dp-row">
                    <div class="dp-key">Actual Job Run Time</div>
                    <div class="dp-value">{{ item.execution_environment.actual_job_runtime }}</div>
                  </div>
                  <div class="dp-row">
                    <div class="dp-key">Fin Time</div>
                    <div class="dp-value">{{ item.execution_environment.fin_time }}</div>
                  </div>
                  <div class="dp-row">
                    <div class="dp-key">Memory</div>
                    <div class="dp-value">{{ item.execution_environment.memory }}</div>
                  </div>
                  <div class="dp-row">
                    <div class="dp-key">NProc Shared</div>
                    <div class="dp-value">{{ item.execution_environment.n_proc_shared }}</div>
                  </div>
                  <div class="dp-row">
                    <div class="dp-key">Fin Time Stamp</div>
                    <div class="dp-value">{{ item.execution_environment.fin_timestamp }}</div>
                  </div>
                </b-card>
              </b-col>
            </b-row>

            <b-row id="calculated-properties" class="m-4" style="padding: 0 15px;">
              <b-card v-if="item.calculated_properties" class="full-width">
                <template #header>
                  <h4 class="mb-0">Calculated Properties</h4>
                </template>
                <b-row>
                  <b-col cols="6">
                    <div class="dp-row">
                      <div class="dp-key">Homos</div>
                      <div class="dp-value">{{ item.calculated_properties.homos }}</div>
                    </div>
                    <div class="dp-row">
                      <div class="dp-key">Energy</div>
                      <div class="dp-value">{{ item.calculated_properties.energy }}</div>
                    </div>
                    <div class="dp-row">
                      <div class="dp-key">Dipole X</div>
                      <div class="dp-value">{{ item.calculated_properties.dipole.x }}</div>
                    </div>
                    <div class="dp-row">
                      <div class="dp-key">Dipole Y</div>
                      <div class="dp-value">{{ item.calculated_properties.dipole.y }}</div>
                    </div>
                    <div class="dp-row">
                      <div class="dp-key">Dipole Z</div>
                      <div class="dp-value">{{ item.calculated_properties.dipole.z }}</div>
                    </div>
                    <div class="dp-row">
                      <div class="dp-key">HF</div>
                      <div class="dp-value">{{ item.calculated_properties.hf }}</div>
                    </div>
                    <div class="dp-row">
                      <div class="dp-key">Homo eigenvalue</div>
                      <div class="dp-value">{{ item.calculated_properties.homo_eigen_value }}</div>
                    </div>
                    <div class="dp-row">
                      <div class="dp-key">Homo eigenvalues</div>
                      <div class="dp-value">
                        <div v-for="(homoEigenvalue, index) in item.calculated_properties.homo_eigen_values" :key="index">
                          {{ homoEigenvalue }}
                        </div>
                      </div>
                    </div>
                  </b-col>
                  <b-col cols="6">
                    <div class="dp-row">
                      <div class="dp-key">Lumo eigenvalue</div>
                      <div class="dp-value">{{ item.calculated_properties.lumo_eigen_value }}</div>
                    </div>
                    <div class="dp-row">
                      <div class="dp-key">Lumo eigenvalues</div>
                      <div class="dp-value">
                        <div v-for="(lumoEigenvalue, index) in item.calculated_properties.lumo_eigen_values" :key="index">
                          {{ lumoEigenvalue }}
                        </div>
                      </div>
                    </div>
                  </b-col>
                </b-row>
              </b-card>
            </b-row>

            <b-row id="structural-formats" class="m-4">
              <b-col cols="6">
                <b-card v-if="item.final_molecule_structural_formats" class="card-component">
                  <template #header>
                    <h4 class="mb-0">Structural Formats</h4>
                  </template>
                  <div class="dp-row">
                    <div class="dp-key">SDF</div>
                    <div class="dp-value">{{ item.final_molecule_structural_formats.sdf }}</div>
                  </div>
                  <div class="dp-row">
                    <div class="dp-key">PDB</div>
                    <div class="dp-value">{{ item.final_molecule_structural_formats.pdb }}</div>
                  </div>
                </b-card>
              </b-col>
            </b-row>

            <b-row id="calculation" class="m-4" style="padding: 0 15px;">
              <b-card v-if="item.calculation" class="full-width">
                <template #header>
                  <h4 class="mb-0">Calculation</h4>
                </template>
                <div class="dp-row">
                  <div class="dp-key">JobStatus</div>
                  <div class="dp-value">{{ item.calculation.job_status }}</div>
                </div>
                <div class="dp-row">
                  <div class="dp-key">Basis</div>
                  <div class="dp-value">{{ item.calculation.basis }}</div>
                </div>
                <div class="dp-row">
                  <div class="dp-key">NMO</div>
                  <div class="dp-value">{{ item.calculation.nmo }}</div>
                </div>
                <div class="dp-row">
                  <div class="dp-key">Keywords</div>
                  <div class="dp-value">{{ item.calculation.keywords }}</div>
                </div>
                <div class="dp-row">
                  <div class="dp-key">Package</div>
                  <div class="dp-value">{{ item.calculation.package }}</div>
                </div>
                <div class="dp-row">
                  <div class="dp-key">CalcType</div>
                  <div class="dp-value">{{ item.calculation.calc_type }}</div>
                </div>
                <div class="dp-row">
                  <div class="dp-key">Methods</div>
                  <div class="dp-value">{{ item.calculation.methods }}</div>
                </div>
              </b-card>
            </b-row>

            <b-row id="identifiers" class="m-4">
              <b-col cols="6">
                <b-card v-if="item.identifiers" class="card-component">
                  <template #header>
                    <h4 class="mb-0">Identifiers</h4>
                  </template>
                  <div class="dp-row">
                    <div class="dp-key">InChIKey</div>
                    <div class="dp-value">{{ item.identifiers.inchi_key }}</div>
                  </div>
                  <div class="dp-row">
                    <div class="dp-key">Canonical SMILES</div>
                    <div class="dp-value">{{ item.identifiers.canonical_smiles }}</div>
                  </div>
                  <div class="dp-row">
                    <div class="dp-key">InChI</div>
                    <div class="dp-value">{{ item.identifiers.inchi }}</div>
                  </div>
                  <div class="dp-row">
                    <div class="dp-key">SMILES</div>
                    <div class="dp-value">{{ item.identifiers.smiles }}</div>
                  </div>
                </b-card>
              </b-col>
            </b-row>

            <b-row id="files" class="m-4" style="padding: 0 15px;">
              <b-card v-if="item.files" class="full-width">
                <template #header>
                  <h4 class="mb-0">Files</h4>
                </template>
                <div class="dp-row">
                  <div class="dp-key">SMILES File</div>
                  <div class="dp-value">{{ item.files.smiles_file }}</div>
                </div>
                <div class="dp-row">
                  <div class="dp-key">SDF Structure File</div>
                  <div class="dp-value">{{ item.files.sdf_structure_file }}</div>
                </div>
                <div class="dp-row">
                  <div class="dp-key">Gaussian Output File</div>
                  <div class="dp-value">{{ item.files.gaussian_output_file }}</div>
                </div>
                <div class="dp-row">
                  <div class="dp-key">Gaussian Input File</div>
                  <div class="dp-value">{{ item.files.gaussian_input_file }}</div>
                </div>
                <div class="dp-row">
                  <div class="dp-key">PDB Structure File</div>
                  <div class="dp-value">{{ item.files.pdb_structure_file }}</div>
                </div>
                <div class="dp-row">
                  <div class="dp-key">InChI File</div>
                  <div class="dp-value">{{ item.files.inchi_file }}</div>
                </div>
              </b-card>
            </b-row>

            <b-row id="input-file-configuration" class="m-4" style="padding: 0 15px;">
              <b-card v-if="item.input_file_configuration" class="full-width">
                <template #header>
                  <h4 class="mb-0">Input File Configuration</h4>
                </template>
                <div class="dp-row">
                  <div class="dp-key">Link0 Commands</div>
                  <div class="dp-value">{{ item.input_file_configuration.link_0_commands }}</div>
                </div>
                <div class="dp-row">
                  <div class="dp-key">Route Commands</div>
                  <div class="dp-value">{{ item.input_file_configuration.route_commands }}</div>
                </div>
              </b-card>
            </b-row>

          </b-container>
        </div>
      </div>
    </div>



  </div>
</template>

<script>
import MolecularStructureImg from "@/components/common/MolecularStructureImg";

const {utils} = AiravataAPI;

export default {
  props: {
    dp: Object
  },
  components: {
    MolecularStructureImg
  },
  data() {
    return {
      item: null,
      showAlert: false,

      sections: [
        {id: "summary", label: "Summary"},
        {id: "execution-environment", label: "Execution Environment"},
        {id: "calculated-properties", label: "Calculated Properties"},
        {id: "structural-formats", label: "Structural Formats"},
        {id: "calculation", label: "Calculation"},
        {id: "identifiers", label: "Identifiers"},
        {id: "files", label: "Files"},
        {id: "input-file-configuration", label: "Input File Configuration"},
      ],
      currentSection: "summary",

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
        this.$router.push({name: 'comp-data-product-list'});
      }, 3000);
    },
    scrollToSection(sectionId) {
      const sectionElement = document.getElementById(sectionId);
      if (sectionElement) {
        sectionElement.scrollIntoView({behavior: "smooth"});
        this.currentSection = sectionId;
      }
    },
  },
};

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
  margin-bottom: 20px;
}

.card-component {
  margin-bottom: 20px;
}


.layout-container {
  display: flex;
  flex-direction: row;
  gap: 20px;
  height: 100vh;
}


.navigation {
  width: 250px;
  background-color: #f8f9fa;
  padding: 15px;
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
  overflow-y: auto;
}

.navigation h2 {
  font-size: 1.2rem;
  margin-bottom: 15px;
  color: #333;
}


.side-nav ul {
  list-style-type: none;
  padding: 0;
  margin: 0;
}


.side-nav li {
  margin-bottom: 10px;
}


.side-nav li a {
  text-decoration: none;
  color: #333;
  font-weight: 400;
  display: block;
  padding: 8px 10px;
  border-radius: 4px;
}


.side-nav li a:hover {
  background-color: #e9ecef;
  color: #0056b3;
}


.side-nav li.active a {
  font-weight: bold;
  background-color: #007bff;
  color: white;
}


.details-content {
  flex: 1;
  padding: 15px;
  overflow-y: auto;
}

</style>

