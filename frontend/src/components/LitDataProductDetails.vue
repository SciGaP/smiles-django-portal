<template>
  <div>
    <b-alert variant="warning" v-model="showAlert">
      Literature Data Product is not found!
    </b-alert>
    <div v-if="item">
      <b-container fluid>
        <b-row class="m-4">
          <b-col cols="6">
            <b-row>
              <b-col>
                <b-card class="card-component">
                  <div class="dp-row">
                    <div class="dp-key">Data Product ID</div>
                    <div class="dp-value">{{ item.data_product_id }}</div>
                  </div>
                  <div class="dp-row">
                    <div class="dp-key">Name</div>
                    <div class="dp-value">{{ item.name }}</div>
                  </div>
                  <div class="dp-row">
                    <div class="dp-key">Search Keywords</div>
                    <div class="dp-value">{{ item.search_keywords }}</div>
                  </div>
                  <div class="dp-row">
                    <div class="dp-key">Redox Info</div>
                    <div class="dp-value">{{ item.redox_info }}</div>
                  </div>
                </b-card>
              </b-col>
            </b-row>
          </b-col>

          <b-col cols="6">
            <b-row>
              <b-col>
                <b-card v-if="item.biblio" class="card-component">
                  <div class="dp-row">
                    <div class="dp-key">DOI</div>
                    <div class="dp-value">{{ item.biblio.doi }}</div>
                  </div>
                  <div class="dp-row">
                    <div class="dp-key">Published Date</div>
                    <div class="dp-value">{{ item.biblio.published_date }}</div>
                  </div>
                  <div class="dp-row">
                    <div class="dp-key">Title</div>
                    <div class="dp-value">{{ item.biblio.title }}</div>
                  </div>
                  <div class="dp-row">
                    <div class="dp-key">Publisher</div>
                    <div class="dp-value">{{ item.biblio.publisher }}</div>
                  </div>
                </b-card>
              </b-col>
            </b-row>
          </b-col>
        </b-row>

        <b-row class="m-4">
          <b-col cols="12">
            <div v-if="item.records">
              <b-table
                  responsive
                  striped
                  hover
                  sticky-header
                  outlined
                  :items="item.records"
                  :fields="fields"
                  stacked="md"
                  small
              >

                <template #cell(structure)="data">
                  <molecular-structure-img :structure="data.item.structure" height="50" width="50"/>
                </template>

                <template #cell(actions)="row">
                  <div class="text-right">
                    <b-button :pressed="row.detailsShowing" size="sm" variant="outline-info"
                              @click="row.toggleDetails">
                      {{ row.detailsShowing ? 'Hide' : 'Show' }} Details
                    </b-button>
                  </div>

                </template>

                <template #row-details="row">
                  <b-card>
                    <lit-record-details :record="row.item"/>
                  </b-card>
                </template>

                <template #table-busy>
                  <div class="text-center text-danger my-2">
                    <b-spinner class="align-middle"></b-spinner>
                    <strong>Loading...</strong>
                  </div>
                </template>

              </b-table>
            </div>
          </b-col>
        </b-row>

      </b-container>
    </div>
  </div>
</template>

<script>
import {configurationService} from "@/services/configuraion-service";
import LitRecordDetails from "./LitRecordDetails"
import MolecularStructureImg from "@/components/common/MolecularStructureImg";

const {utils} = AiravataAPI;

export default {
  props: {
    dp: Object
  },
  components: {
    LitRecordDetails,
    MolecularStructureImg
  },
  data() {
    return {
      item: null,
      showAlert: false
    };
  },
  computed: {
    fields() {
      return configurationService.getLitRecordDisplayableColumns();
    }
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
      utils.FetchUtils.get(`/smiles/lit-dp/${this.$route.params.id}`)
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
        this.$router.push({name: 'data-product-list', query: {type: 'lit'}});
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

.card-component {
  margin-bottom: 20px;
}

</style>

