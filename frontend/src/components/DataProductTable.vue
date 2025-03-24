<template>
  <!-- Container -->
  <div class="w-full p-4">

    <!-- Header: New Button and Search Bar -->
    <div class="flex justify-between items-center mb-4">
      <!-- Search Bar -->
      <div class="relative w-full mr-4">
        <input
          id="filter-input"
          v-model="filter"
          type="search"
          placeholder="Type to Search"
          class="w-full pl-10 pr-4 py-2 rounded-md border border-gray-300 focus:outline-none focus:border-blue-500"
        >
        <img src="../assets/icons/search-icon.svg" alt="Search" class="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-500">
      </div>
      <!-- New Button -->
      <button @click="redirectToUpload" class="flex items-center bg-blue-600 text-white px-4 py-2 rounded-md border border-blue-600 hover:bg-blue-700">
        <!-- New Plus Icon -->
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4" />
        </svg>
        <!-- New Text -->
        <span class="font-medium">New</span>
      </button>
      <!-- Share Button -->
      <button
        @click="openShareModal"
        :disabled="selectedItems.length === 0"
        class="flex items-center bg-green-600 text-white px-4 py-2 rounded-md border border-green-600 hover:bg-green-700 disabled:opacity-50"
      >
        <!-- Share Icon -->
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
          <path stroke-linecap="round" stroke-linejoin="round" d="M15 8a3 3 0 11-6 0 3 3 0 016 0zm0 0v7m-6-7v7m6-3H9" />
        </svg>
        <span class="font-medium">Share</span>
      </button>
    </div>

    <!-- Table and Sidebar -->
    <div class="flex">

      <!-- Table -->
      <div :class="['overflow-x-auto overflow-y-auto border border-gray-300 rounded-md bg-white', selectedRow ? 'w-2/3' : 'w-full']" style="max-height: 70vh;">
        <table class="min-w-full relative">
          <!-- Table Head -->
          <thead class="bg-gray-100 sticky top-0">
          <tr>
            <!-- Select All -->
            <th class="px-4 py-2 border-b border-gray-300">
              <input type="checkbox" :checked="selectAll" @click.stop @change="toggleSelectAll" />
            </th>            
            <th v-for="field in fields" :key="field.key" class="px-4 py-2 text-left text-gray-600 border-b border-gray-300">
              {{ field.label || field.key }}
            </th>
          </tr>
          </thead>
          <!-- Table Body -->
          <tbody>
            <tr v-for="item in paginatedItems" :key="item.data_product_id" :class="{'bg-gray-50': selectedItems.includes(item.data_product_id)}" @click="onRowClicked(item)" @dblclick="onRowDoubleClicked(item)" class="hover:bg-gray-100 cursor-pointer transition-colors duration-200">
            <!-- Select One -->
            <td class="px-4 py-2 border-b border-gray-200">
              <input
                type="checkbox"
                :checked="selectedItems.includes(item.data_product_id)"
                @click.stop
                @change="toggleSelectItem(item.data_product_id)"
              />
            </td>
            <td v-for="field in fields" :key="field.key" class="px-4 py-2 border-b border-gray-200">
              <!-- Custom Cell Template -->
              <div v-if="field.key === 'structure'">
                <molecular-structure-img :structure="item.structure" height="50" width="50"/>
              </div>
              <div v-else>
                {{ getValueByPath(item, field.key) }}
              </div>
            </td>
          </tr>
          <!-- Empty State -->
          <tr v-if="!items.length && !isBusy">
            <td colspan="100%" class="text-center py-4 text-gray-500">No data available</td>
          </tr>
          </tbody>
        </table>
        <!-- Loading Spinner -->
        <div v-if="isBusy" class="flex items-center justify-center py-4 text-blue-500">
          <svg class="animate-spin h-5 w-5 mr-2" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z"></path>
          </svg>
          <strong>Loading...</strong>
        </div>
      </div>

      <!-- Sidebar -->
      <div v-if="selectedRow" class="w-1/3 border border-gray-300 rounded-md bg-white ml-4" style="max-height: 70vh;">
        <home-page-structure-view :dp="selectedRow" :key="selectedRow"/>
      </div>

    </div>

    <!-- Pagination -->
    <div class="flex justify-end mt-4 mb-4">
      <div class="my-1 pr-5">
        <div class="flex items-center space-x-2">
          <button @click="prevPage" :disabled="currentPage === 1" class="px-3 py-1 bg-white border border-gray-300 rounded-md hover:bg-gray-100 disabled:opacity-50 transition-colors duration-200">
           Back
          </button>
          <span class="text-gray-700">Page {{ currentPage }} of {{ totalPages }}</span>
          <button @click="nextPage" :disabled="currentPage === totalPages" class="px-3 py-1 bg-white border border-gray-300 rounded-md hover:bg-gray-100 disabled:opacity-50 transition-colors duration-200">
            Next
          </button>
        </div>
      </div>
    </div>

    <!-- Share Modal -->
    <div v-if="showShareModal" class="fixed inset-0 bg-gray-500 bg-opacity-75 flex justify-center items-center z-50">
      <div class="bg-white p-6 rounded-lg shadow-lg w-1/3">
        <h3 class="text-lg font-bold mb-4">Share Data Products</h3>
        <label for="share-type" class="block mb-2">Share with:</label>
        <select id="share-type" v-model="shareType" class="w-full mb-4 border rounded-md p-2">
          <option value="user">User</option>
          <option value="group">Group</option>
        </select>
        <label for="share-target" class="block mb-2">User/Group ID:</label>
        <el-autocomplete
          id="share-target"
          v-model="shareTarget"
          placeholder="Enter user or group ID"
          :fetch-suggestions="fetchSuggestions"
          @select="onSelectSuggestion"
          :trigger-on-focus="true"
          :clearable="true"
          class="w-full mb-4"
        />
        <div class="flex justify-end space-x-4">
          <button @click="closeShareModal" class="px-4 py-2 bg-gray-300 rounded-md hover:bg-gray-400">Cancel</button>
          <button @click="submitShare" class="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700">Submit</button>
        </div>
      </div>
    </div>


  </div>
</template>

<script>
import { configurationService } from "@/services/configuraion-service";
import MolecularStructureImg from "@/components/common/MolecularStructureImg";
import HomePageStructureView from "@/components/HomePageStructureView.vue";
import plusButtonIcon from "@/assets/icons/plus.svg";

const { utils } = AiravataAPI;

export default {
  name: "SMILESDataProductTable",
  components: {
    MolecularStructureImg,
    HomePageStructureView,
  },
  props: {
    type: {
      type: String,
      default: "lit",
    },
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
      totalPages: 1,

      selectedItems: [],
      selectAll: false,
      showShareModal: false,
      shareType: "user",
      shareTarget: "",
      suggestions: [],
      isLoadingSuggestions: false,
    };
  },
  computed: {
    fields() {
      return configurationService.getDisplayableColumns(this.type);
    },
    filteredItems() {
      if (!this.filter) {
        return this.items;
      }
      const filter = this.filter.toLowerCase();
      return this.items.filter((item) => {
        return Object.values(item).some((value) => {
          return String(value).toLowerCase().includes(filter);
        });
      });
    },
    paginatedItems() {
      return this.items;
    },
  },
  watch: {
    filter() {
      this.currentPage = 1;
      this.updateTotalPages();
    },
    items() {
      this.updateTotalPages();
    },
    perPage() {
      this.updateTotalPages();
    },
  },
  mounted() {
    this.loadSMILESDataProducts();
  },
  methods: {
    toggleSelectAll() {
    this.selectAll = !this.selectAll;
    if (this.selectAll) {
      this.selectedItems = this.paginatedItems.map(item => item.data_product_id);
    } else {
      this.selectedItems = [];
    }
  },
  toggleSelectItem(itemId) {
    const index = this.selectedItems.indexOf(itemId);
    if (index > -1) {
      this.selectedItems.splice(index, 1);
    } else {
      this.selectedItems.push(itemId);
    }
    const allSelected = this.paginatedItems.length > 0 &&
      this.paginatedItems.every(item => this.selectedItems.includes(item.data_product_id));
    this.selectAll = allSelected;
  },
  openShareModal() {
  if (this.selectedItems.length === 0) {
    alert("Please select at least one data product.");
    return;
  }
  this.showShareModal = true;
  this.fetchSuggestions("", () => {});
  },
  closeShareModal() {
    this.showShareModal = false;
    this.shareTarget = "";
  },
  submitShare() {
    if (!this.shareTarget) {
      alert("Please specify a user or group.");
      return;
    }
    const requestData = {
      data_product_ids: this.selectedItems,
      share_type: this.shareType,
      share_target: this.shareTarget,
    };
    fetch("/smiles/share-data-product", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(requestData),
    })
    .then(response => response.json())
    .then(data => {
      if (data.error) {
        alert("Error: " + data.error);
      } else {
        alert("Data products shared successfully!");
        this.closeShareModal();
      }
    })
    .catch(error => {
      console.error("Error:", error);
    });
  },
  async fetchSuggestions(queryString, callback) {
    try {
      //shareType (user/group)
      const typeParam = this.shareType;  

      const response = await fetch(`/smiles/action/?action=search&type=${typeParam}&query=${encodeURIComponent(queryString || "")}`);
      const data = await response.json();

      let suggestions = [];
      if (typeParam === 'user') {
        suggestions = data.users.map(user => ({
          value: user.id,  // internalUserId
          label: user.name,
          type: 'user',
        }));
      } else if (typeParam === 'group') {
        suggestions = data.groups.map(group => ({
          value: group.name,
          label: group.id,
          type: 'group',
        }));
      }
      callback(suggestions);
    } catch (error) {
      console.error("Error fetching suggestions:", error);
      callback([]);
    }
  },
  onSelectSuggestion(selected) {
    this.shareTarget = selected.value;
  },

    getValueByPath(obj, path) {
    if (!obj || !path) return "";
    // for every key
    return path.split('.').reduce((acc, key) => acc && acc[key], obj);
    },      
    loadSMILESDataProducts() {
      this.isBusy = true;
      utils.FetchUtils.get(`/smiles/${this.type}-dps?page=${this.currentPage}&size=${this.perPage}`).then((response) => {
        console.log("Server response:", response);
        if (response) {
        this.items = response.data_products; 
        this.totalRows = response.total_count;
        this.updateTotalPages();
        }
        this.isBusy = false;
      });
    },
    updateTotalPages() {
      this.totalPages = Math.ceil(this.totalRows / this.perPage) || 1;
    },
    onRowClicked(item) {
      if (this.selectedRow) {
        this.$set(this.selectedRow, "_rowVariant", "");
      }

      if (this.selectedRow === item) {
        this.selectedRow = null;
      } else {
        this.$set(item, "_rowVariant", "secondary");
        this.selectedRow = item;
      }
      this.toggleSelectItem(item.data_product_id);
    },
    onRowDoubleClicked(item) {
      this.$router.push({
        name: this.type + "-data-product-detailed",
        params: { type: this.type.toString(), id: item.data_product_id, dp: item },
      });
    },
    redirectToUpload() {
      this.$router.push({ name: "data-product-upload", params: { dp_type: this.type } });
    },
    prevPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
        this.loadSMILESDataProducts();
      }
    },
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++;
        this.loadSMILESDataProducts();
      }
    },
  },
};
</script>

<style>
</style>