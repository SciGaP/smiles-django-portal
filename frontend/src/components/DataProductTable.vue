<template>
  <b-container fluid>
    <b-row class="d-flex justify-content-end mt-2 mr-2 mb-0">
      <b-col lg="auto" xs="12">
        <b-button variant="primary" @click="redirectToUpload">
          <img :src="plusButtonIcon" alt="Plus Button Icon" class="icon">
          New
        </b-button>
      </b-col>
    </b-row>

    <b-row class="d-flex justify-content-center">
      <b-col lg="8" class="my-3">
        <b-form-group>
          <b-input-group>
            <div class="position-relative">
              <b-form-input id="filter-input"
                            v-model="filter"
                            type="search"
                            placeholder="Type to Search"
                            class="rounded-pill pl-5 search-bar"
              ></b-form-input>
              <img src="../assets/icons/search-icon.svg" alt="Search" class="position-absolute search-icon">
            </div>
          </b-input-group>
        </b-form-group>
      </b-col>
    </b-row>

    <b-row>
      <div class="table-container" :class="{ 'table-container-reduced': selectedRow }">
        <div style="margin-top: 60px;">
          <b-table
              responsive
              hover
              sticky-header
              :items="items"
              :fields="fields"
              :current-page="currentPage"
              :per-page="perPage"
              :filter="filter"
              stacked="md"
              show-empty
              small
              @filtered="onFiltered"
              :busy="isBusy"
              @row-clicked="onRowClicked"
              @row-dblclicked="onRowDoubleClicked"
          >

            <template #cell(structure)="data">
              <molecular-structure-img :structure="data.item.structure" height="50" width="50"/>
            </template>

            <template #table-busy>
              <div class="text-center text-danger my-2">
                <b-spinner class="align-middle"></b-spinner>
                <strong>Loading...</strong>
              </div>
            </template>

          </b-table>
        </div>
      </div>

      <div v-if="selectedRow" class="sidebar">
        <home-page-structure-view :dp="selectedRow" :key="selectedRow"/>
      </div>
    </b-row>

    <div class="pagination-container">
      <b-row class="mb-4">
        <b-col sm="7" md="3" class="my-1 ml-auto pr-5">
          <b-pagination
              v-model="currentPage"
              :total-rows="totalRows"
              :per-page="perPage"
              prev-text="< Prev"
              next-text="Next >"
              align="right"
              size="sm"
              pills
              class="my-0"
          ></b-pagination>
        </b-col>
      </b-row>
    </div>
  </b-container>
</template>

<script>
import {configurationService} from "@/services/configuraion-service";
import MolecularStructureImg from "@/components/common/MolecularStructureImg";
import HomePageStructureView from "@/components/HomePageStructureView.vue"
import plusButtonIcon from '@/assets/icons/plus.svg';

const {utils} = AiravataAPI;

export default {
  name: "SMILESDataProductTable",
  components: {
    MolecularStructureImg,
    HomePageStructureView
  },
  props: {
    type: {
      type: String,
      default: "lit"
    }
  },
  data() {
    return {
      items: [],
      totalRows: 1,
      currentPage: 1,
      perPage: 20,
      filter: null,
      isBusy: true,
      plusButtonIcon,
      selectedRow: null,
    }
  },
  computed: {
    fields() {
      return configurationService.getDisplayableColumns(this.type);
    }
  },
  mounted() {
    this.loadSMILESDataProducts();
  },
  methods: {
    loadSMILESDataProducts() {
      utils.FetchUtils.get(`/smiles/${this.type}-dps?page=${this.currentPage}&size=${this.perPage}`)
          .then(response => {
            if (response) {
              this.items = response;
              // Set the initial number of items
              this.totalRows = this.items.length
            }
          });
      this.isBusy = false;
    },
    onFiltered(filteredItems) {
      // Trigger pagination to update the number of buttons/pages due to filtering
      this.totalRows = filteredItems.length
      this.currentPage = 1
    },
    onRowClicked(item) {
      if (this.selectedRow) {
        this.$set(this.selectedRow, '_rowVariant', '');
      }

      if (this.selectedRow === item) {
        this.selectedRow = null;
      } else {
        this.$set(item, '_rowVariant', 'secondary');
        this.selectedRow = item;
      }
    },
    onRowDoubleClicked(item) {
      this.$router.push({
        name: this.type + '-data-product-detailed',
        params: {type: this.type.toString(), id: item.data_product_id, dp: item}
      })
    },
    redirectToUpload() {
      this.$router.push({name: 'data-product-upload', params: {dp_type: this.type}});
    }
  }
}
</script>

<style scoped>
.table-container,
.table-container-reduced {
  overflow-x: scroll;
  overflow-y: auto;
  border: 1px solid gray;
  border-radius: 20px;
  margin: 5px 10px;
  background: white;
  max-height: 73vh;
  width: 100vw;
  transition: width 0.5s ease;
}

.table-container-reduced {
  width: 60vw;
}

.search-bar {
  width: 60vw;
}

.search-icon {
  left: 15px;
  top: 50%;
  transform: translateY(-50%);
  width: 20px;
  height: 20px;
}

.pagination-container {
  text-align: right;
  height: 10%;
}

.sidebar {
  right: 0;
  min-width: 33vw;
  z-index: 1;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.2);
  border: 1px solid gray;
  border-radius: 20px;
  margin: 5px 5px 5px 5px;
  background: white;
  max-height: 73vh;
}

</style>