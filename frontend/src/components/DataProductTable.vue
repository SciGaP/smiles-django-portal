<template>
  <b-container fluid>
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

    <div class="table-container">
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
        >
          <template #cell(actions)="row">
            <div class="text-right">
              <b-button :pressed="row.detailsShowing" size="sm" variant="outline-info" @click="row.toggleDetails">
                {{ row.detailsShowing ? 'Hide' : 'Show' }} Details
              </b-button>
            </div>

          </template>

          <template #row-details="row">
            <b-card>
              <pre>{{ formattedJson(row) }}</pre>
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
    </div>

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

const {utils} = AiravataAPI;

export default {
  name: "SMILESDataProductTable",
  data() {
    return {
      items: [],
      totalRows: 1,
      currentPage: 1,
      perPage: 20,
      filter: null,
      type: this.$route.query.type,
      isBusy: true,
    }
  },
  computed: {
    fields() {
      return configurationService.getDisplayableColumns(this.type);
    },
    formattedJson() {
      return (row) => {
        return JSON.stringify(row.item, null, 2);
      };
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
      this.$router.push({
        name: this.type + '-data-product-detailed',
        params: {type: this.type.toString(), id: item.data_product_id, dp: item}
      })
    }
  }
}
</script>

<style>
.table-container {
  overflow-x: scroll;
  overflow-y: auto;
  border: 1px solid gray;
  border-radius: 20px;
  margin: 5px 10px;
  background: white;
  max-height: 73vh;
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

</style>